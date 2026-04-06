import pdfplumber
import json
import os

def generar_menu():
    pdf_path = 'carta.pdf'
    
    # Esto nos va a decir en el log de GitHub si el archivo existe
    if not os.path.exists(pdf_path):
        print(f"ERROR: No se encuentra el archivo {pdf_path} en el repositorio.")
        print(f"Archivos presentes: {os.listdir('.')}") # Listamos qué hay para debuguear
        exit(1) # Forzamos un error claro

    menu_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(horizontal_ltr=True, y_tolerance=3)
                
                lines = {}
                for w in words:
                    y = round(w['top'])
                    if y not in lines: lines[y] = []
                    lines[y].append(w)
                
                for y in sorted(lines.keys()):
                    line_words = sorted(lines[y], key=lambda x: x['x0'])
                    texto_linea = " ".join([w['text'] for w in line_words])
                    
                    ultimo_w = line_words[-1]
                    # Ajustamos el umbral a 350 por si la hoja es angosta
                    if ultimo_w['x0'] > 350 and any(char.isdigit() for char in ultimo_w['text']):
                        precio = ultimo_w['text']
                        nombre = " ".join([w['text'] for w in line_words[:-1]])
                        menu_data.append({"nombre": nombre, "precio": precio})
                    else:
                        menu_data.append({"seccion": texto_linea})

        with open('menu.json', 'w', encoding='utf-8') as f:
            json.dump(menu_data, f, ensure_ascii=False, indent=4)
        print("¡JSON generado con éxito!")

    except Exception as e:
        print(f"Error procesando el PDF: {e}")
        exit(1)

if __name__ == "__main__":
    generar_menu()