from abc import ABC, abstractmethod
from typing import Tuple
from app.domain.entities import Candidate, JobOffer
from app.domain.repositories import CandidateRepository

class LLMService(ABC):
    """
    Interfaz (Puerto) para el servicio del modelo de IA.
    La capa de infraestructura implementará este contrato.
    """
    @abstractmethod
    def evaluate_compatibility(self, candidate_skills: str, job_description: str) -> Tuple[float, str, str, str, str]:
        pass

class JobMatcher:
    """
    Caso de Uso: Calcula la compatibilidad entre el Perfil Interno y una Oferta.
    """
    def __init__(self, llm_service: LLMService, candidate_repo: CandidateRepository):
        # Inyección de puerto LLM y Repositorio Dominio
        self._llm_service = llm_service
        self._candidate_repo = candidate_repo

    def calculate_fit(self, offer: JobOffer, habilidades_adicionales: str = "") -> Tuple[float, str, str, str, str]:
        """
        Calcula el 'fit' obteniendo de forma autónoma a nuestro candidato
        y luego usando el LLM de la infraestructura inyectada.
        """
        # Obtenemos al candidato desde Base de datos / JSON (Repository)
        candidate = self._candidate_repo.get_candidate_profile()
        
        if not candidate:
            return 0.0, "Operación detenida. Imposible leer el perfil propio del Candidato."
            
        # (Sin debug prints en producción)

        # Preparación del contexto para el LLM
        candidate_context = ", ".join(candidate.habilidades) if candidate.habilidades else "Sin habilidades especificadas."
        if habilidades_adicionales:
            candidate_context += f"\n\nHabilidades Adicionales desde Web: {habilidades_adicionales}"
        
        offer_context = (
            f"Cargo: {offer.titulo}\n"
            f"Empresa: {offer.empresa}\n"
            f"Descripción: {offer.descripcion}\n"
            f"Requerimientos: {', '.join(offer.habilidades)}"
        )
        
        # Delegamos en nuestro puerto LLM
        porcentaje, resumen, technical_pros, improvement_areas, market_relevance = self._llm_service.evaluate_compatibility(
            candidate_skills=candidate_context, 
            job_description=offer_context
        )
        
        porcentaje_validado = max(0.0, min(100.0, float(porcentaje)))
        return porcentaje_validado, resumen, technical_pros, improvement_areas, market_relevance
