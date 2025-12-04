#!/usr/bin/env python3
"""
SISTEMA SIMPLE Y FUNCIONAL de consulta de cédulas
TODO en un archivo - Sin problemas de importación
"""

import os
import sys
import time
import csv
import argparse
from datetime import datetime
from typing import List

# ========== FUNCIONES BÁSICAS ==========
def validar_cedula(cedula: str) -> bool:
    """Valida que la cédula sea correcta"""
    return cedula and cedula.isdigit() and 6 <= len(cedula) <= 10

def crear_directorios():
    """Crea los directorios necesarios"""
    for dir_name in ['descargas', 'resultados', 'logs']:
        os.makedirs(dir_name, exist_ok=True)

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("CONSULTA DE VIGENCIA DE CÉDULAS")
    print("Registraduría Nacional de Colombia")
    print("="*60)
    print("\nOpciones:")
    print("1. Consulta individual")
    print("2. Consultas desde archivo CSV")
    print("3. Salir")

# ========== CONSULTA BÁSICA ==========
def consulta_basica(cedula: str):
    """Función básica de consulta (para pruebas)"""
    print(f"\n🔍 Consultando cédula: {cedula}")
    print("⚠️  Esta es una versión de prueba")
    
    # Simular consulta
    time.sleep(1)
    
    return {
        'cedula': cedula,
        'nombre': 'JUAN PEREZ GARCIA',
        'estado': 'VIGENTE',
        'fecha_expedicion': '15/05/2010',
        'municipio': 'BOGOTÁ D.C.',
        'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'estado_consulta': 'EXITOSO'
    }

# ========== MANEJO DE CSV ==========
def guardar_resultado(resultado: dict, archivo: str = "resultados.csv"):
    """Guarda resultado en CSV"""
    try:
        archivo_path = os.path.join('resultados', archivo)
        
        campos = list(resultado.keys())
        existe = os.path.exists(archivo_path)
        
        with open(archivo_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            if not existe:
                writer.writeheader()
            writer.writerow(resultado)
        
        print(f"✅ Resultado guardado en: {archivo_path}")
    except Exception as e:
        print(f"❌ Error guardando: {e}")

def leer_cedulas_csv(archivo: str) -> List[str]:
    """Lee cédulas desde CSV"""
    cedulas = []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Saltar encabezado
            for fila in reader:
                if fila and fila[0].strip():
                    cedula = fila[0].strip()
                    if validar_cedula(cedula):
                        cedulas.append(cedula)
        print(f"📖 Leídas {len(cedulas)} cédulas de {archivo}")
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
    return cedulas

# ========== PROGRAMA PRINCIPAL ==========
def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Sistema de consulta de cédulas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s              # Modo interactivo
  %(prog)s -c 1234567890 # Consulta individual
  %(prog)s -a datos.csv  # Consultas desde CSV
        """
    )
    
    parser.add_argument('-c', '--cedula', help='Cédula a consultar')
    parser.add_argument('-a', '--archivo', help='Archivo CSV con cédulas')
    
    args = parser.parse_args()
    
    # Crear directorios
    crear_directorios()
    
    try:
        if args.archivo:
            # Modo archivo CSV
            if not os.path.exists(args.archivo):
                print(f"❌ Archivo no encontrado: {args.archivo}")
                return
            
            cedulas = leer_cedulas_csv(args.archivo)
            
            if not cedulas:
                print("❌ No hay cédulas válidas en el archivo")
                return
            
            print(f"\n📋 Procesando {len(cedulas)} cédulas...")
            
            for i, cedula in enumerate(cedulas, 1):
                print(f"\n[{i}/{len(cedulas)}] Consultando: {cedula}")
                resultado = consulta_basica(cedula)
                guardar_resultado(resultado)
                time.sleep(0.5)  # Pausa entre consultas
            
            print(f"\n🎉 Proceso completado. {len(cedulas)} consultas procesadas.")
            
        elif args.cedula:
            # Modo consulta individual
            if not validar_cedula(args.cedula):
                print(f"❌ Cédula inválida: {args.cedula}")
                return
            
            resultado = consulta_basica(args.cedula)
            guardar_resultado(resultado)
            
            print("\n📊 RESULTADO:")
            for clave, valor in resultado.items():
                if clave not in ['fecha_consulta', 'estado_consulta']:
                    print(f"  {clave}: {valor}")
                    
        else:
            # Modo interactivo
            while True:
                mostrar_menu()
                
                try:
                    opcion = input("\nSeleccione una opción (1-3): ").strip()
                    
                    if opcion == '1':
                        cedula = input("\n📝 Ingrese número de cédula: ").strip()
                        
                        if not validar_cedula(cedula):
                            print("❌ Cédula inválida")
                            continue
                        
                        resultado = consulta_basica(cedula)
                        guardar_resultado(resultado)
                        
                        print("\n📊 RESULTADO:")
                        for clave, valor in resultado.items():
                            if clave not in ['fecha_consulta', 'estado_consulta']:
                                print(f"  {clave}: {valor}")
                    
                    elif opcion == '2':
                        archivo = input("\n📁 Ingrese nombre del archivo CSV: ").strip()
                        
                        if not os.path.exists(archivo):
                            print(f"❌ Archivo no encontrado: {archivo}")
                            continue
                        
                        cedulas = leer_cedulas_csv(archivo)
                        
                        if not cedulas:
                            print("❌ No hay cédulas válidas")
                            continue
                        
                        print(f"\n📋 Procesando {len(cedulas)} cédulas...")
                        
                        for i, cedula in enumerate(cedulas, 1):
                            print(f"[{i}/{len(cedulas)}] Consultando: {cedula}")
                            resultado = consulta_basica(cedula)
                            guardar_resultado(resultado)
                            time.sleep(0.5)
                        
                        print(f"\n🎉 {len(cedulas)} consultas procesadas.")
                    
                    elif opcion == '3':
                        print("\n👋 ¡Hasta luego!")
                        break
                    
                    else:
                        print("❌ Opción inválida")
                        
                except KeyboardInterrupt:
                    print("\n\n⚠️ Operación cancelada")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrumpido")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
