import pytesseract
from PIL import Image
import json
import re
import os

# CONFIGURACIÓN DE RUTA (Verificá que sea esta)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_carta():
    imagen_input = 'carta.jpg' # El nombre que exportás de Illustrator
    
    if not os.path.exists(imagen_input):
        print(f"Error: No se encuentra '{imagen_input}' en esta carpeta.")
        return

    print("Leyendo el diseño de Illustrator... (OCR en progreso)")
    
    try:
        # Ejecutamos el OCR en español
        texto = pytesseract.image_to_string(Image.open(imagen_input), lang='spa')
        
        menu_json = []
        
        for linea in texto.split('\n'):
            # --- LIMPIEZA DE PUNTOS ---
            # Borramos cadenas de 2 o más puntos, guiones o espacios extra
            linea = re.sub(r'\.{2,}', ' ', linea)
            linea = re.sub(r'_{2,}', ' ', linea)
            linea = linea.strip()

            if len(linea) < 3: continue

            # Buscamos el precio (Números de 2 a 6 dígitos, opcional con $)
            match_precio = re.search(r'(\$?\s?\d{2,6})', linea)
            
            if match_precio:
                precio = match_precio.group(1).strip()
                # El nombre es lo que queda, quitando el precio y basura del final
                nombre = linea.replace(precio, '').strip().rstrip('. -_')
                
                if nombre:
                    menu_json.append({"nombre": nombre, "precio": precio})
            else:
                # Si no tiene precio, lo guardamos como Sección (ej: "ENTRADAS")
                menu_json.append({"seccion": linea})

        # Guardamos el resultado
        with open('menu.json', 'w', encoding='utf-8') as f:
            json.dump(menu_json, f, ensure_ascii=False, indent=4)
        
        print(f"¡Éxito! Se generó 'menu.json' con {len(menu_json)} items.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    procesar_carta()