import pdfplumber
import json
import os

#
def generar_menu():
    pdf_path = 'carta.pdf' # El archivo que vas a subir
    if not os.path.exists(pdf_path):
        return

    menu_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extraemos palabras con sus coordenadas
            words = page.extract_words(horizontal_ltr=True, y_tolerance=3)
            
            # Agrupamos palabras por línea (misma coordenada Y)
            lines = {}
            for w in words:
                y = round(w['top'])
                if y not in lines:
                    lines[y] = []
                lines[y].append(w)
            
            # Procesamos cada línea
            for y in sorted(lines.keys()):
                line_words = sorted(lines[y], key=lambda x: x['x0'])
                texto_linea = " ".join([w['text'] for w in line_words])
                
                # Lógica: Si el último elemento de la línea está muy a la derecha, es el precio
                # Ajustá el valor 400 según el ancho de tu PDF
                ultimo_w = line_words[-1]
                if ultimo_w['x0'] > 400 and any(char.isdigit() for char in ultimo_w['text']):
                    precio = ultimo_w['text']
                    nombre = " ".join([w['text'] for w in line_words[:-1]])
                    menu_data.append({"nombre": nombre, "precio": precio})
                else:
                    # Es un título de sección o descripción
                    menu_data.append({"seccion": texto_linea})

    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generar_menu()