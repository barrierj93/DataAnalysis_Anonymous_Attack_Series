# Script tonto para eliminar caracteres sobrantes del 
# archivo csv (Draft_AnonymousAttacks.csv)

import csv
import re

def clean_csv(input_path, output_path):
    with open(input_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Eliminar todos los corchetes con números dentro en cada columna
            cleaned_row = [re.sub(r'\s*\[\d+\]\s*', '', cell) for cell in row]
            writer.writerow(cleaned_row)

def main():
    input_path = input("Ingrese la ruta del archivo de entrada: ")
    output_folder = input("Ingrese la ruta de la carpeta de salida: ")
    output_filename = input("Ingrese el nombre del archivo de salida (sin extensión): ")
    
    output_path = f"{output_folder}/{output_filename}.csv"

    clean_csv(input_path, output_path)
    print(f"Archivo limpio guardado en: {output_path}")

if __name__ == "__main__":
    main()