# Web Scraping (wikipedia) para obtener un csv con
# los datos necesitados del grupo Anonymous


import csv
import requests
from bs4 import BeautifulSoup

# Pedir la URL y el nombre del archivo CSV
url_html = input("Ingresa la URL del archivo HTML: ")
ruta_csv = input("Ingresa la ruta donde se guardará el archivo CSV: ")
nombre_csv = input("Ingresa el nombre del archivo CSV (sin extensión): ")

# Realizar la petición HTTP para obtener el contenido del HTML
response = requests.get(url_html)
response.raise_for_status()  # Levanta un error si la petición no es exitosa

# Analizar el contenido HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Crear una lista para almacenar los datos
data = []

# Variables para almacenar el año y el título actuales
current_year = ""
current_title = ""

# Buscar todos los elementos <div> con clase mw-heading
sections = soup.find_all('div', class_='mw-heading')

for section in sections:
    if 'mw-heading2' in section['class']:
        # Es un nuevo año
        current_year = section.get_text(strip=True)
        current_title = ""  # Resetear el título para el caso donde no haya
        sibling = section.find_next_sibling()
        
        # Manejar casos antes de 2011 donde el cuerpo del incidente está dentro de <li>
        if sibling and sibling.name == 'ul':
            for li in sibling.find_all('li'):
                description = li.get_text(strip=True)
                data.append([current_year, "Sin título", description])
                
    elif 'mw-heading3' in section['class']:
        # Es un nuevo incidente con título
        current_title = section.get_text(strip=True)
        description = ""
        sibling = section.find_next_sibling()
        
        # Recorrer los hermanos siguientes para construir la descripción
        while sibling and not any('mw-heading' in cls for cls in sibling.get('class', [])):
            if sibling.name == 'p':
                # Manipular <a href> dentro de <p> para añadir espacios antes y después
                for a in sibling.find_all('a'):
                    a.insert_before(' ')
                    a.insert_after(' ')
                description += sibling.get_text() + " "  # Eliminar strip() para preservar los espacios
            sibling = sibling.find_next_sibling()

        # Limpiar y agregar los datos a la lista
        description = description.strip()
        if current_year and description:
            data.append([current_year, current_title, description])

# Guardar los datos en un archivo CSV usando punto y coma como delimitador
csv_file = f"{ruta_csv}/{nombre_csv}.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['Año', 'Título', 'Descripción'])
    writer.writerows(data)

print(f"Archivo CSV guardado en: {csv_file}")
