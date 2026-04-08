import os
import json
import google.generativeai as genai
from typing import Tuple
from app.use_cases.matchmaker import LLMService

class GeminiService(LLMService):
    """
    Adaptador concreto del puerto LLMService.
    Se comunica con la API de Google Generative AI (Gemini).
    """
    def __init__(self):
        from dotenv import load_dotenv
        # Cargar variables de entorno directamente al inicio de la clase (Supervisión)
        load_dotenv()
        
        # 1. Asegurarse de leer la API KEY del .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRÍTICO: La variable de entorno GEMINI_API_KEY no está configurada o el .env no fue cargado correctamente.")
        
        # 2. Configurar el SDK
        genai.configure(api_key=api_key)
        
        # Definimos el mecanismo de fallback ordenado del más moderno al más clásico
        self.models_to_try = [
            'gemini-2.5-pro',
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-pro',
            'gemini-1.0-pro'
        ]

    def evaluate_compatibility(self, candidate_skills: str, job_description: str) -> Tuple[float, str, str, str]:
        # Prompt de Ingeniería Robusto diseñado para hacer match profundo
        prompt = f"""
        Actúa como un evaluador de recursos humanos técnico, objetivo e imparcial especializado en perfiles estratégicos.
        Tu misión es evaluar la idoneidad y habilidades transferibles del candidato hacia la vacante. Tienes la RESTRICCIÓN ABSOLUTA Y ESTRICTA de sugerir o priorizar cargos orientados a "Software Developer", "Fullstack", "Backend" o programación pura. No queremos perfiles técnicos puros en el Top 10.
        El usuario es un Ingeniero Civil Industrial y tu foco debe ser 100% estratégico de Gestión. Prioriza fuertemente: Key Account Manager (KAM), Product Owner, Project Manager y Gerencia de Operaciones/E-commerce/TI.
        REGLA DE ORO: Si el CV menciona lenguajes como 'Python' o código, debes tratarlos explícitamente como "herramientas avanzadas de análisis de datos y mejora de procesos (Business Intelligence)", NO como habilidades de desarrollador de software.
        
        --- PERFIL DEL CANDIDATO ---
        Habilidades y Competencias Declaradas: {candidate_skills}
        
        --- DATOS DE LA VACANTE ---
        {job_description}
        
        --- INSTRUCCIONES ---
        Realiza un análisis técnico estricto comparando el perfil del candidato con los requisitos de la vacante.
        Evalúa la coincidencia de habilidades técnicas, experiencia relevante y brechas de competencia.
        Sé objetivo, no hagas referencia a metas personales, objetivos geográficos ni aspiraciones individuales.
        
        Devuelve EXCLUSIVAMENTE un bloque JSON válido (sin texto ni markdown adicional):
        {{
            "percentage": <número entre 0.0 y 100.0 representando el nivel de idoneidad técnica>,
            "summary": "<Resumen ejecutivo objetivo de máximo 3 oraciones sobre el nivel de adecuación del candidato a la vacante>",
            "technical_pros": "<Competencias técnicas del candidato que coinciden con los requisitos de la vacante>",
            "improvement_areas": "<Brechas técnicas identificadas: habilidades requeridas que el candidato no demuestra tener>",
            "market_relevance": "<Evaluación objetiva de la relevancia del cargo para el desarrollo profesional técnico del candidato en el mercado laboral actual>"
        }}
        """
        
        response_text = None
        last_error = None
        
        # Bucle de Respaldo (Fallback Mechanism)
        for model_name in self.models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                response_text = response.text.strip()
                print(f"--- ÉXITO AL USAR MODELO: {model_name} ---") # Debug en terminal
                break # Si llegamos aquí, fue exitoso, no necesitamos otros modelos
            except Exception as e:
                last_error = e
                pass # Silently fallback
                continue
                
        if not response_text:
            return 0.0, f"Error crítico: Ningún modelo funcionó. Error: {str(last_error)}", "Error", "Error", "Error"
            
        try:
            # Sanitizar posibles formatos Markdown (como bloques de código '```json') antes de parsear
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            # Convertimos e instanciamos a JSON
            data = json.loads(response_text.strip())
            
            # Extraemos de forma segura asegurando cast
            percentage = float(data.get("percentage", 0.0))
            summary = str(data.get("summary", "Sin resumen disponible."))
            technical_pros = str(data.get("technical_pros", "No identificados."))
            improvement_areas = str(data.get("improvement_areas", "No identificadas."))
            market_relevance = str(data.get("market_relevance", "No evaluado."))
            
            return percentage, summary, technical_pros, improvement_areas, market_relevance
            
        except json.JSONDecodeError as jde:
            return 0.0, f"Error en el formato de salida: {str(jde)}", "Error", "Error", "Error"
        except Exception as e:
            # Fallback seguro que no rompe la cadena de Arquitectura Limpia
            # Error silenciado en producción
            return 0.0, f"Error real: {str(e)}", "Error", "Error", "Error"
