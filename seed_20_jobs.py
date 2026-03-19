import sqlite3
import random
from datetime import datetime, timedelta
import os

DB_PATH = "data/discoveries.db"

# Sample data for realistic IT jobs
empresas = ["Google", "Amazon Web Services", "Microsoft", "Meta", "Apple", "Netflix", "Spotify", "Mercado Libre", "Globant", "Cornershop", "NotCo", "Fintual", "Buk", "Kavak", "Nubank", "Falabella", "Cencosud", "Latam Airlines", "Banco de Chile", "BCI"]
cargos = ["Senior Software Engineer", "Cloud Architect", "Data Scientist", "DevOps Engineer", "Machine Learning Engineer", "Frontend Developer (React)", "Backend Developer (Python/Go)", "Tech Lead", "Full Stack Developer", "Site Reliability Engineer (SRE)"]
plataformas = ["LinkedIn", "Laborum", "Indeed", "Glassdoor", "Get on Board"]
market_relevances = [
    "Altamente relevante. Expande tu alcance como arquitecto de roles distribuidos en LATAM.",
    "Alineado con tus habilidades core. Gran proyección hacia liderazgo técnico.",
    "Excelente oportunidad para ganar exposición en arquitecturas serverless escalables.",
    "Potencial para desarrollar skills críticos requeridos en el mercado tecnológico actual.",
    "Te posicionaría muy bien en ecosistemas de datos a escala global."
]

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
with sqlite3.connect(DB_PATH) as conn:
    # Clear existing data so we have exactly 20 (or we can just append, but let's clear to be clean)
    conn.execute("DELETE FROM offer_results")
    
    for i in range(20):
        # Generate random high scores since the user wants a good looking dashboard
        # Let's group them: A few top matches (95-100), some good ones (75-90), some average (40-70)
        if i < 3:
            score = random.uniform(90.0, 99.9)
        elif i < 10:
            score = random.uniform(75.0, 89.9)
        else:
            score = random.uniform(40.0, 74.9)
            
        empresa = random.choice(empresas)
        cargo = random.choice(cargos)
        plataforma = random.choice(plataformas)
        relevance = random.choice(market_relevances)
        
        # Random date within the last 15 days
        past_date = datetime.now() - timedelta(days=random.randint(0, 15), hours=random.randint(0, 23))
        
        conn.execute("""
            INSERT INTO offer_results
                (titulo, empresa, plataforma, match_percentage, summary,
                 technical_pros, improvement_areas, market_relevance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cargo, 
            empresa, 
            plataforma, 
            score, 
            f"El perfil demuestra sólida experiencia aplicable a los requerimientos de {empresa}.",
            "Experiencia con Python, AWS, Docker nativo. Conocimientos de arquitectura de microservicios probados.",
            "Requiere familiarización con la herramienta interna específica de la empresa. Podría necesitar certificación adicional.",
            relevance,
            past_date.isoformat()
        ))
    
    conn.commit()

print("Base de datos poblada con 20 ofertas de prueba.")
