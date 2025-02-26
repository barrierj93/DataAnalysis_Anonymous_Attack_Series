import csv
import os

def leer_diccionario(ruta_diccionario):
    with open(ruta_diccionario, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f if linea.strip()]

def buscar_coincidencias(fila, diccionario):
    return '; '.join(palabra for palabra in diccionario if palabra.lower() in fila.lower())

def procesar_csv(ruta_entrada, ruta_salida, diccionario, nombre_columna):
    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as archivo_entrada, \
         open(ruta_salida, 'w', newline='', encoding='utf-8') as archivo_salida:
        
        lector = csv.reader(archivo_entrada, delimiter=';')
        escritor = csv.writer(archivo_salida, delimiter=';')
        
        encabezados = next(lector)
        encabezados.append(nombre_columna)
        escritor.writerow(encabezados)
        
        for fila in lector:
            coincidencias = buscar_coincidencias(';'.join(fila), diccionario)
            fila.append(coincidencias)
            escritor.writerow(fila)

def main():
    ruta_diccionario = input("Introduce la ruta del archivo de diccionario (.txt): ")
    ruta_csv_entrada = input("Introduce la ruta del archivo CSV de entrada: ")
    ruta_salida = input("Introduce la ruta para el archivo de salida: ")
    nombre_columna = input("Introduce el nombre para la nueva columna: ")
    nombre_archivo_salida = input("Introduce el nombre para el archivo de salida (sin .csv): ")
    
    ruta_csv_salida = os.path.join(ruta_salida, f"{nombre_archivo_salida}.csv")
    
    diccionario = leer_diccionario(ruta_diccionario)
    procesar_csv(ruta_csv_entrada, ruta_csv_salida, diccionario, nombre_columna)
    
    print(f"Proceso completado. El archivo de salida se encuentra en: {ruta_csv_salida}")

if __name__ == "__main__":
    main()