import requests
import json

BASE = "http://127.0.0.1:5000"

batch = [
    {
        "titulo": "Ingeniero de Software Backend",
        "empresa": "TechGlobal Dublin",
        "descripcion": "Empresa europea busca Python/Flask developer para oficinas en Irlanda. Trabajo en equipos distribuidos internacionales.",
        "plataforma": "LinkedIn"
    },
    {
        "titulo": "Arquitecto de Soluciones Cloud",
        "empresa": "AWS Partner SA",
        "descripcion": "Buscamos arquitecto con experiencia en AWS, Terraform y CI/CD para liderar proyectos de migración a la nube.",
        "plataforma": "Laborum"
    },
    {
        "titulo": "Desarrollador Full Stack",
        "empresa": "StartupX",
        "descripcion": "Startup requiere desarrollador Frontend React y Backend Flask con experiencia básica.",
        "plataforma": "Indeed"
    }
]

print("--- Enviando batch POST /api/v1/discovery ---")
r = requests.post(f"{BASE}/api/v1/discovery", json=batch, headers={"Content-Type": "application/json"})
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

print("\n--- GET /api/v1/discoveries ---")
r2 = requests.get(f"{BASE}/api/v1/discoveries")
print(f"Status: {r2.status_code}")
data = r2.json()
print(f"Total registros: {data.get('count', 0)}")
for item in data.get('data', []):
    print(f"  [{item['match_percentage']}%] {item['titulo']} @ {item['empresa']} ({item['plataforma']})")
