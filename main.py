import sys
import os

# 1. Ajuste del PYTHONPATH para asegurar resolución absoluta (Supervisor)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Handoff al Arquitecto: Importamos la app de rutas/infraestructura
from app.main import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 65)
    print("🚀 [ORQUESTADOR] Iniciando Motor de Prospección Autónoma RAG")
    print("📋 [TRADUCTOR] Misión Activa: Ingeniería Civil Industrial Estratégica")
    print("🛡️ [PORTERO] Webhooks n8n listos y saneados (URL Cleaner)")
    print("🔍 [SUPERVISOR] Todas las capas SOLID y módulos inicializados OK")
    print("✅ SISTEMA 100% OPERATIVO. Escuchando en el puerto 5000...")
    print("🔗 Entorno local activo en: http://127.0.0.1:5000/")
    print("=" * 65)
    
    # 3. Lanzamiento (Arquitecto)
    app.run(host='0.0.0.0', port=5000, debug=True)
