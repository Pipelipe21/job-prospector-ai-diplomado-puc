import requests
import time

API_URL = "http://127.0.0.1:5000/api/v1/discovery"

# Crear ofertas de perfiles estratégicos
ofertas_estrategicas = {
    "ofertas": [
        {
            "titulo": "Key Account Manager (KAM) B2B",
            "empresa": "Mercado Libre",
            "descripcion": "Buscamos un KAM para liderar la estrategia B2B comercial, manejar grandes cuentas clave corporativas y alinear objetivos de negocio con desarrollos tecnológicos. Requiere visión estratégica, negociación y liderazgo.",
            "plataforma": "LinkedIn",
            "habilidades": ["Negociación", "Estrategia Comercial", "B2B", "Liderazgo", "Análisis de Datos"],
            "url": "https://linkedin.com/jobs/view/12345"
        },
        {
            "titulo": "Product Owner Senior",
            "empresa": "Banco Falabella",
            "descripcion": "Rol crítico para la tribu de Tarjetas de Crédito. Trabajar el roadmap del producto, priorizar el backlog en metodologías ágiles y servir de puente entre el equipo técnico y las gerencias de negocio.",
            "plataforma": "Get on Board",
            "habilidades": ["Scrum", "Agile", "Roadmapping", "Visión de Producto", "Fintech"],
            "url": "https://getonbrd.com/jobs/12345"
        },
        {
            "titulo": "Project Manager Office (PMO) Infraestructura",
            "empresa": "Cencosud",
            "descripcion": "Estamos buscando un PMO que lidere los proyectos de infraestructura retail a nivel regional. Capacidad para gestionar presupuesto, cronogramas, riesgos y comunicación con stakeholders clave (Dirección General).",
            "plataforma": "Laborum",
            "habilidades": ["Gestión de Proyectos", "PMI", "Stakeholder Management", "Presupuestos"],
            "url": "https://laborum.cl/job/12"
        },
        {
            "titulo": "Ecommerce Manager LATAM",
            "empresa": "Falabella.com",
            "descripcion": "Responsable del crecimiento transversal del canal online, definiendo KPIs de venta, conversión y experiencia de usuario. Requiere fuerte background en procesos logísticos, operaciones comerciales y marketing digital.",
            "plataforma": "LinkedIn",
            "habilidades": ["Ecommerce", "Logística", "Sales", "Performance", "KPI"],
            "url": "https://linkedin.com/jobs/view/999"
        },
        {
            "titulo": "Líder de Mejora Continua y Procesos",
            "empresa": "Soprole",
            "descripcion": "Ingeniero Civil Industrial con foco en la mejora continua de la cadena de suministro. Certificación Lean Six Sigma deseable. Capacidad de automatizar procesos con analítica avanzada de datos e influir en la eficiencia de la planta.",
            "plataforma": "Trabajando",
            "habilidades": ["Lean Six Sigma", "Supply Chain", "Optimización", "Procesos Industriales"],
            "url": "https://trabajando.cl/empleo/333"
        }
    ]
}

print("Inyectando 5 ofertas estratégicas (KAM, PO, PM) al Motor de Evaluacion Gemini...")
response = requests.post(API_URL, json=ofertas_estrategicas)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.text)
