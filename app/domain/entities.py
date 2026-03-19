from dataclasses import dataclass, field
from typing import List

@dataclass
class JobOffer:
    titulo: str
    empresa: str
    descripcion: str
    habilidades: List[str] = field(default_factory=list)

@dataclass
class Candidate:
    nombre: str
    habilidades: List[str] = field(default_factory=list)
