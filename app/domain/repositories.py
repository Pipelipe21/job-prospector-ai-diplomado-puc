from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Candidate

class CandidateRepository(ABC):
    """
    Puerto de Salida (Outbound Port) para obtener los datos del candidato.
    Permite que la capa de Caso de Uso no dependa de si leemos de JSON, DB o API.
    """
    @abstractmethod
    def get_candidate_profile(self) -> Optional[Candidate]:
        """
        Retorna la entidad Candidate. 
        Si el repositorio falla o no hay perfil, retorna None de forma segura.
        """
        pass
