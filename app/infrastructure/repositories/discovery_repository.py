import sqlite3
import os
from datetime import datetime
from typing import List, Dict

DB_PATH = "data/discoveries.db"

class DiscoveryRepository:
    """
    Repositorio de Infraestructura para almacenar y consultar resultados
    de la evaluación de idoneidad técnica de ofertas laborales.
    """

    def __init__(self, db_path: str = DB_PATH):
        self._db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la BD con el schema neutral de evaluación técnica."""
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        with sqlite3.connect(self._db_path) as conn:
            # Crear tabla si no existe (no hacer drop)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS offer_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    empresa TEXT NOT NULL,
                    plataforma TEXT DEFAULT 'General',
                    match_percentage REAL DEFAULT 0.0,
                    summary TEXT,
                    technical_pros TEXT,
                    improvement_areas TEXT,
                    market_relevance TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_result(self, titulo: str, empresa: str, plataforma: str,
                    match_percentage: float, summary: str,
                    technical_pros: str, improvement_areas: str,
                    market_relevance: str) -> int:
        """Guarda un resultado de evaluación técnica en la BD."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO offer_results
                    (titulo, empresa, plataforma, match_percentage, summary,
                     technical_pros, improvement_areas, market_relevance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (titulo, empresa, plataforma, match_percentage, summary,
                  technical_pros, improvement_areas, market_relevance,
                  datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid

    def get_all_results(self) -> List[Dict]:
        """Retorna todos los resultados ordenados por % de idoneidad descendente."""
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM offer_results 
                ORDER BY match_percentage DESC, created_at DESC
            """).fetchall()
            return [dict(r) for r in rows]
