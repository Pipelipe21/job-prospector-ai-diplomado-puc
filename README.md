# Motor de Prospección Autónoma

Sistema de Análisis de Compatibilidad Laboral impulsado por Inteligencia Artificial (Google Gemini) y automatización de flujos de trabajo (n8n). El sistema evalúa de manera objetiva perfiles de candidatos contra ofertas del mercado, generando un ranking de oportunidades en tiempo real.

---

## 🏛️ Arquitectura del Sistema

El proyecto sigue principios de **Clean Architecture** (Dominio, Casos de Uso, Infraestructura) y se compone de las siguientes capas tecnológicas:

1. **Frontend (UI Premium)**: Interfaz responsiva moderna construida con Bootstrap 5, CSS Grid y micro-interacciones. Consumo de API mediante Fetch asíncrono.
2. **Backend (Flask)**: Servidor Python ligero que expone endpoints REST (`/upload_cv`, `/api/v1/sync-search`, `/api/v1/discoveries`).
3. **Motor de Prospección (n8n)**: Encargado de recibir el webhook de búsqueda emitido por el backend, consultar plataformas externas y enviar las vacantes detectadas de vuelta al pipeline.
4. **Motor de Inferencia (Google Gemini)**: Procesamiento de Lenguaje Natural (LLM) que actúa como Evaluador Técnico de Recursos Humanos, extrayendo *Competencias Compatibles*, *Brechas* y analizando la *Idoneidad de Mercado*.
5. **Persistencia (SQLite)**: Base de datos ligera y veloz (`discoveries.db`) para almacenar localmente los resultados de las evaluaciones asíncronas y renderizarlas en el dashboard del cliente. Generada automáticamente en `/data`.

---

## 🚀 Guía de Instalación Rápida

### 1. Prerrequisitos
- Python 3.9+
- Clave de API válida de Google Gemini.
- (Opcional) Instancia de n8n operativa para recibir el webhook de prospección.

### 2. Clonar y Preparar Entorno
```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd <nombre-del-proyecto>

# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Cree un archivo `.env` en la raíz del proyecto tomando como referencia el `.env.example` interno, declarando:

```env
GEMINI_API_KEY="AIzaSy...su-clave..."
N8N_WEBHOOK_URL="https://su-instancia-n8n.cloud/webhook/sync-search"
```

### 5. Ejecutar la Aplicación
```bash
python -m app.main
```

Abra el explorador en `http://127.0.0.1:5000/`.

---

## 🛡️ Principio de Neutralidad Absoluta
La aplicación está programada con directrices de *Prompt Engineering* estrictas que garantizan análisis funcionales sin sesgo territorial, subjetivo o preferencial. Los criterios evaluativos se remiten enteramente a las matrices de perfiles técnicos del candidato frente a las descripciones de cargo (Job Descriptions).
