import os
import shutil
from fuzzywuzzy import fuzz

def organizar_descargas():
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Mapeo de extensiones a subcarpetas
    subcarpetas_extensiones = {
        "Documentos": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
        "Imágenes": [".jpg", ".jpeg", ".png", ".gif"],
        "Vídeos": [".mp4", ".mov", ".avi"],
        "Programas": [".exe", ".msi"],
        "Comprimidos": [".zip", ".rar", ".7z"],
        "Otros": []
    }

    # Mapeo de palabras clave a subcarpetas
    subcarpetas_palabras_clave = {
        "Diplomas": ["diploma"],
        "EPIS": ["epis"],
        "Seguridad Social": ["ita", "rnt", "rlc"]
    }

    for archivo in os.listdir(carpeta_descargas):
        ruta_archivo = os.path.join(carpeta_descargas, archivo)

        if os.path.isfile(ruta_archivo):
            movido = False

            # Primero, intentar mover el archivo según palabras clave en el nombre
            for subcarpeta, palabras_clave in subcarpetas_palabras_clave.items():
                for palabra in palabras_clave:
                    # Comparar similitud entre la palabra clave y el nombre del archivo
                    if fuzz.partial_ratio(palabra.lower(), archivo.lower()) > 80:  # Umbral de similitud (80%)
                        carpeta_destino = os.path.join(carpeta_descargas, subcarpeta)
                        os.makedirs(carpeta_destino, exist_ok=True)
                        shutil.move(ruta_archivo, os.path.join(carpeta_destino, archivo))
                        movido = True
                        break
                if movido:
                    break
            
            # Si el archivo no se movió por nombre, intentar moverlo por extensión
            if not movido:
                extension = os.path.splitext(archivo)[1].lower()
                for subcarpeta, extensiones in subcarpetas_extensiones.items():
                    if extension in extensiones:
                        carpeta_destino = os.path.join(carpeta_descargas, subcarpeta)
                        os.makedirs(carpeta_destino, exist_ok=True)
                        shutil.move(ruta_archivo, os.path.join(carpeta_destino, archivo))
                        movido = True
                        break

            # Si no se movió por nombre ni por extensión, moverlo a "Otros"
            if not movido:
                carpeta_destino = os.path.join(carpeta_descargas, "Otros")
                os.makedirs(carpeta_destino, exist_ok=True)
                shutil.move(ruta_archivo, os.path.join(carpeta_destino, archivo))

if __name__ == "__main__":
    organizar_descargas()
