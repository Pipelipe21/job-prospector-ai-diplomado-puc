import json
import os
import PyPDF2
import requests as http_client
import urllib.parse
from flask import Blueprint, request, jsonify, current_app, render_template
from app.domain.entities import JobOffer, Candidate
from app.use_cases.matchmaker import JobMatcher
from app.infrastructure.repositories.discovery_repository import DiscoveryRepository

# URL del webhook de n8n (puede sobreescribirse con variable de entorno N8N_WEBHOOK_URL)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/sync-search")

_discovery_repo = DiscoveryRepository()

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web_bp.route('/upload_cv', methods=['POST'])
def upload_cv():
    try:
        if 'cv' not in request.files:
            return jsonify({"error": "No se adjuntó archivo PDF"}), 400
            
        cv_file = request.files['cv']
        if cv_file.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400
            
        pdf_reader = PyPDF2.PdfReader(cv_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
            
        repo_path = "data/perfil_candidato.json"
        if os.path.exists(repo_path):
            with open(repo_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['cv_text'] = extracted_text.strip()
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
        return jsonify({"status": "success", "message": f"Extraídos {len(extracted_text)} caracteres del documento."})
    except Exception as e:
        return jsonify({"error": f"Error procesando PDF: {str(e)}"}), 500

def clean_url(url: str) -> str:
    """Extrae el link real y lo decodifica de proxies de google.com/url."""
    url = str(url).strip()
    original_url = url
    if 'google.com/url' in url:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'q' in qs:
            url = qs['q'][0]
    
    final_url = urllib.parse.unquote(url)
    if original_url != final_url:
        print(f"🔗 [PORTERO_FIX] Decoded URL from {original_url} to {final_url}")
    return final_url

def __find_job_fields(obj):
    """
    Busca de forma recursiva (Smart Parser) en un diccionario o lista
    los campos 'titulo', 'empresa' y 'descripcion'.
    Retorna un diccionario con estos datos si los encuentra, None en caso contrario.
    """
    if isinstance(obj, dict):
        if 'titulo' in obj and 'empresa' in obj and 'descripcion' in obj:
            return {
                'titulo': str(obj['titulo']).strip(),
                'empresa': str(obj['empresa']).strip(),
                'descripcion': str(obj['descripcion']).strip(),
                'habilidades': obj.get('habilidades', []),
                'url': clean_url(obj.get('url', ''))
            }
        for value in obj.values():
            result = __find_job_fields(value)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = __find_job_fields(item)
            if result:
                return result
    return None

@api_bp.route('/match', methods=['POST'])
def match_endpoint():
    """
    Endpoint HTTP que recibe los datos de n8n.
    Solo espera la Oferta Laboral. El candidato se auto-calcula in-house.
    """
    data = request.get_json(silent=True) or {}
    
    # Solo para debug: print(f"\n[SUPERVISOR] Request JSON recibido...")

    if not data:
        return jsonify({"error": "Payload JSON ausente o mal formado."}), 400

    try:
        # Lógica de 'Portero': usar el Smart Parser para buscar en cualquier nivel del payload
        offer_data = __find_job_fields(data)

        # Validación estricta del Portero contra n8n:
        if not offer_data or not offer_data['titulo'] or not offer_data['empresa'] or not offer_data['descripcion']:
             return jsonify({
                 "error": "El servidor rechazó la petición. Asegurate de enviar campos con datos no vacíos para 'titulo', 'empresa' y 'descripcion' (pueden estar dentro del nodo de n8n)."
             }), 400

        # Mapeo a dominio puro
        job_offer = JobOffer(
            titulo=offer_data['titulo'],
            empresa=offer_data['empresa'],
            descripcion=offer_data['descripcion'],
            habilidades=offer_data['habilidades']
        )

        job_matcher: JobMatcher = current_app.config.get('JOB_MATCHER')
        if not job_matcher:
            return jsonify({"error": "Servicio interno (JobMatcher) no disponible o mal enlazado en flask"}), 500

        extra_skills = data.get('habilidades_adicionales', '')

        # Llamada central asilada.
        porcentaje, resumen, technical_pros, improvement_areas, market_relevance = job_matcher.calculate_fit(job_offer, extra_skills)

        # Formatear la respuesta
        return jsonify({
            "status": "success",
            "data": {
                "match_percentage": porcentaje,
                "summary": resumen,
                "technical_pros": technical_pros,
                "improvement_areas": improvement_areas,
                "market_relevance": market_relevance
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error interno en el procesamiento HTTP: {str(e)}"}), 500


@api_bp.route('/discovery', methods=['POST'])
def discovery_endpoint():
    """
    Endpoint Masivo: Recibe una lista de ofertas desde n8n, 
    procesa cada una con Gemini y persiste los resultados en SQLite.
    """
    raw = request.get_json(silent=True) or []
    # Solo para debug: print(f"\n[SUPERVISOR] /discovery payload recibido...")

    job_matcher: JobMatcher = current_app.config.get('JOB_MATCHER')
    if not job_matcher:
        return jsonify({"error": "Servicio interno (JobMatcher) no disponible."}), 500

    # Normalizar: aceptar lista raiz o lista dentro de 'ofertas'
    if isinstance(raw, dict):
        offers_list = raw.get('ofertas', [raw])
    elif isinstance(raw, list):
        offers_list = raw
    else:
        return jsonify({"error": "Se esperaba una lista de ofertas o un objeto con clave 'ofertas'."}), 400

    results = []
    errors = []

    for i, item in enumerate(offers_list):
        offer_data = __find_job_fields(item)
        if not offer_data:
            errors.append({"index": i, "reason": "No se encontraron campos titulo/empresa/descripcion"})
            continue

        try:
            job_offer = JobOffer(
                titulo=offer_data['titulo'],
                empresa=offer_data['empresa'],
                descripcion=offer_data['descripcion'],
                habilidades=offer_data.get('habilidades', [])
            )
            plataforma = offer_data.get('plataforma', item.get('plataforma', 'General'))

            porcentaje, resumen, technical_pros, improvement_areas, market_relevance = job_matcher.calculate_fit(job_offer)

            record_id = _discovery_repo.save_result(
                titulo=job_offer.titulo,
                empresa=job_offer.empresa,
                plataforma=plataforma,
                match_percentage=porcentaje,
                summary=resumen,
                technical_pros=technical_pros,
                improvement_areas=improvement_areas,
                market_relevance=market_relevance,
                url=offer_data.get('url')
            )
            results.append({"id": record_id, "titulo": job_offer.titulo, "empresa": job_offer.empresa, "match_percentage": porcentaje})
        except Exception as e:
            errors.append({"index": i, "titulo": offer_data.get('titulo', '?'), "reason": str(e)})

    return jsonify({
        "status": "success",
        "processed": len(results),
        "errors": len(errors),
        "results": results,
        "error_details": errors
    }), 200


@api_bp.route('/discoveries', methods=['GET'])
def get_discoveries():
    """Retorna todos los resultados de descubrimiento almacenados en SQLite."""
    try:
        all_results = _discovery_repo.get_all_results()
        return jsonify({"status": "success", "count": len(all_results), "data": all_results}), 200
    except Exception as e:
        return jsonify({"error": f"Error consultando resultados: {str(e)}"}), 500


@api_bp.route('/sync-search', methods=['POST'])
def sync_search():
    """
    Portero Outbound: Lee el perfil del candidato desde disco
    y lo envía al webhook de n8n para iniciar la búsqueda autónoma de ofertas.
    """
    body = request.get_json(silent=True) or {}
    habilidades_adicionales = body.get('habilidades_adicionales', '')

    # Leer perfil del candidato (CV + habilidades base)
    candidate_context = {}
    repo_path = "data/perfil_candidato.json"
    if os.path.exists(repo_path):
        try:
            with open(repo_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            candidate_context = {
                "nombre": profile_data.get("nombre", "Candidato"),
                "habilidades": profile_data.get("habilidades", []),
                "estudios": profile_data.get("estudios", ""),
                "experiencia": profile_data.get("experiencia", ""),
                "cv_text": profile_data.get("cv_text", ""),
                "habilidades_adicionales": habilidades_adicionales,
                "search_operators": "(site:laborum.cl OR site:trabajando.cl OR site:computrabajo.com OR site:linkedin.com OR site:indeed.cl OR site:getonbrd.com OR site:bne.cl OR site:empleospublicos.cl OR site:chiletrabajos.cl OR site:firstjob.me OR site:adecco.cl) after:2026-03-01",
                "limit": 20,
                "time_range": "past_week"
            }
        except Exception as e:
            return jsonify({"error": f"Error leyendo perfil del candidato: {str(e)}"}), 500

    # Enviar perfil al webhook de n8n
    webhook_url = N8N_WEBHOOK_URL
    # print(f"\n[SUPERVISOR] /sync-search → Enviando perfil a n8n: {webhook_url}\n")

    try:
        resp = http_client.post(
            webhook_url,
            json=candidate_context,
            timeout=10
        )
        return jsonify({
            "status": "dispatched",
            "message": f"Perfil enviado al motor de prospección (n8n). Estado: {resp.status_code}",
            "webhook_status": resp.status_code
        }), 200
    except http_client.exceptions.ConnectionError:
        # El webhook no existe todavía (URL de ejemplo) — devolver OK para no bloquear demo
        # print("[SUPERVISOR] Webhook de n8n no alcanzable. Modo demo activado.")
        return jsonify({
            "status": "dispatched",
            "message": "Perfil preparado. Configure N8N_WEBHOOK_URL para activar la prospección real.",
            "webhook_status": 0
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al contactar el webhook: {str(e)}"}), 500
