import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1/match"

payloads = [
    {
        "name": "Flat JSON",
        "data": {
            "titulo": "Ingeniero Backend Senior",
            "empresa": "TechCorp",
            "descripcion": "Buscamos desarrollador con experiencia en Python y Flask.",
            "habilidades": ["Python", "Flask", "API"]
        }
    },
    {
        "name": "n8n Dictionary (Wrap in 'json')",
        "data": {
            "json": {
                "titulo": "Arquitecto de Software",
                "empresa": "InnovaSoft",
                "descripcion": "Diseño de sistemas distribuidos y microservicios.",
                "habilidades": ["Arquitectura", "Microservicios"]
            }
        }
    },
    {
        "name": "n8n List",
        "data": [
            {
                "json": {
                    "titulo": "Ingeniero Cloud",
                    "empresa": "CloudNet",
                    "descripcion": "Manejo de AWS y automatización de despliegues.",
                    "habilidades": ["AWS", "Terraform", "CI/CD"]
                }
            }
        ]
    }
]

for test in payloads:
    print(f"--- Prueba Opcional ({test['name']}) ---")
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(BASE_URL, json=test["data"], headers=headers)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print("Response:", response.text)
    except requests.exceptions.ConnectionError:
        print(f"¡Error! No se pudo conectar al servidor local en {BASE_URL}. Asegúrate que está corriendo.")
    print("-" * 40, "\n")
