import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

print("--- Paso 1: Test /upload_cv ---")
try:
    with open("dummy_cv.pdf", "rb") as f:
        files = {"cv": f}
        response = requests.post(f"{BASE_URL}/upload_cv", files=files)
        print(f"Status: {response.status_code}")
        print("Response:", response.json())
except Exception as e:
    print("Error /upload_cv:", e)

print("\n--- Paso 2: Test /api/v1/match ---")
payload = {
    "titulo": "Ingeniero Backend API",
    "empresa": "SaaS Platform Inc.",
    "descripcion": "Requerimos experto en Python, AWS y Docker para diseñar APIs escalables. Deseable conocimiento en Flask y Serverless.",
    "habilidades_adicionales": "Certificación AWS Solutions Architect, experiencia en microservicios."
}
headers = {"Content-Type": "application/json"}
try:
    response = requests.post(f"{BASE_URL}/api/v1/match", json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("Error /api/v1/match:", e)
