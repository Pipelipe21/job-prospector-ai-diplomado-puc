import json
import os
from typing import Optional
from app.domain.repositories import CandidateRepository
from app.domain.entities import Candidate

class FileCandidateRepository(CandidateRepository):
    """
    Adaptador de Infraestructura que implementa CandidateRepository.
    Lee los datos físicos desde un archivo JSON estructurado de forma local.
    """
    def __init__(self, filepath: str = "data/perfil_candidato.json"):
        self._filepath = filepath

    def get_candidate_profile(self) -> Optional[Candidate]:
        if not os.path.exists(self._filepath):
            print(f"[ERROR DE CAPA DE DATOS]: Archivo maestro de Candidato '{self._filepath}' no encontrado.")
            return None
            
        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Aplanamos la información para suministrarla enriquecida a las habilidades del Candidate (Contexto RAG Local)
            base_skills = data.get("habilidades", [])
            formacion = f"Estudios: {data.get('estudios', '')}"
            historial = f"Experiencia: {data.get('experiencia', '')}"
            cv_text = f"Texto Extraído del CV PDF: {data.get('cv_text', '')}" if 'cv_text' in data else ""
            
            # El "RAG local": Le damos al modelo de lenguaje todo esto bajo la llave habilidades de entidad original.
            contexto_completo = base_skills + [formacion, historial]
            if cv_text:
                contexto_completo.append(cv_text)
            
            return Candidate(
                nombre=data.get("nombre", "Sin Nombre"),
                habilidades=contexto_completo
            )

        except json.JSONDecodeError:
            print(f"[ERROR DE CAPA DE DATOS]: El formato JSON en '{self._filepath}' está corrupto corrupto o es inválido.")
            return None
        except Exception as e:
            print(f"[ERROR FATAL]: Fallo inesperado leyendo perfil: {str(e)}")
            return None
