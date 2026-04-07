import os
import zipfile

def create_secure_backup():
    zip_name = 'Entrega_1_Backup_Final_Carlos_Donoso_Daza.zip'
    
    # Directorios y archivos sensibles o pesados a excluir del ZIP offline
    EXCLUDE_DIRS = {'.git', 'venv', 'env', '__pycache__', '.idea', '.vscode', 'tmp', 'data'}
    EXCLUDE_FILES = {'.env', '.env.local', zip_name, 'zip_backup.py', 'seed_20_jobs.py'}
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modificamos la lista in-place para que os.walk no entre a carpetas prohibidas
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES or file.endswith('.pyc'):
                    continue
                file_path = os.path.join(root, file)
                # Guardamos la ruta relativa dentro del zip
                arcname = os.path.relpath(file_path, start='.')
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    create_secure_backup()
    print(f"Empaquetado completado de forma segura.")
