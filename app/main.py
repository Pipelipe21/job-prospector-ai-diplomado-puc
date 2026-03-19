import os
from dotenv import load_dotenv
from flask import Flask
from app.infrastructure.api.routes import api_bp, web_bp
from app.use_cases.matchmaker import JobMatcher
from app.infrastructure.services.gemini_service import GeminiService
from app.infrastructure.repositories.file_candidate_repository import FileCandidateRepository

def create_app() -> Flask:
    """Factory para crear y ensamblar los componentes de la aplicación."""
    load_dotenv()
    
    app = Flask(__name__)

    # 1. Instanciar Infraestructura Externa (Google Gemini)
    try:
        llm_service = GeminiService()
    except ValueError as e:
        print(f"Error de inicialización: {e}")
        raise e
        
    # 2. Instanciar Repositorio de Perfil Propio (Lectura de JSON)
    candidate_repo = FileCandidateRepository()
    
    # 3. Ensamblar Caso de Uso, Inyectando Múltiples Dependencias
    job_matcher = JobMatcher(
        llm_service=llm_service, 
        candidate_repo=candidate_repo
    )
    
    # 4. Registrar de global para Routes
    app.config['JOB_MATCHER'] = job_matcher

    # 5. Registrar Routes
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    return app

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(host='0.0.0.0', port=5000, debug=True)
