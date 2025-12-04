import sys
import os
import logging
from datetime import datetime
from typing import Optional
import argparse

# Agregar src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from registraduria.flujo import ejecutar_flujo
from storage.csv_storage import CSVStorage
from utils.helpers import validar_cedula, formatear_fecha

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/consulta_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Consulta de vigencia de cédula - Registraduría Nacional')
    parser.add_argument('--cedula', type=str, help='Número de cédula a consultar')
    parser.add_argument('--fecha-expedicion', type=str, help='Fecha de expedición (DD/MM/YYYY)')
    parser.add_argument('--archivo', type=str, help='Archivo CSV con múltiples consultas')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless (sin interfaz gráfica)')
    parser.add_argument('--paralelo', type=int, default=1, help='Número de consultas paralelas')
    
    args = parser.parse_args()
    
    # Crear directorio de salida si no existe
    os.makedirs('output', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    storage = CSVStorage('output/resultados.csv')
    
    if args.archivo:
        # Procesar archivo con múltiples consultas
        import pandas as pd
        try:
            df = pd.read_csv(args.archivo)
            logger.info(f"Procesando {len(df)} consultas desde archivo {args.archivo}")
            
            resultados = []
            for _, row in df.iterrows():
                cedula = str(row.get('cedula', '')).strip()
                fecha = str(row.get('fecha_expedicion', '')).strip()
                
                if not cedula:
                    logger.warning(f"Fila {_}: Cédula vacía, omitiendo")
                    continue
                
                logger.info(f"Consultando cédula: {cedula}")
                resultado = ejecutar_flujo(cedula, fecha, headless=args.headless)
                
                if resultado:
                    resultados.append(resultado)
                    storage.guardar(resultado)
                    logger.info(f"Consulta exitosa para cédula: {cedula}")
                else:
                    logger.error(f"Consulta fallida para cédula: {cedula}")
            
            logger.info(f"Procesamiento completado. {len(resultados)} consultas exitosas.")
            
        except Exception as e:
            logger.error(f"Error al procesar archivo: {e}")
    
    elif args.cedula:
        # Consulta individual
        if not validar_cedula(args.cedula):
            logger.error(f"Cédula inválida: {args.cedula}")
            return
        
        fecha_formateada = formatear_fecha(args.fecha_expedicion) if args.fecha_expedicion else None
        
        logger.info(f"Iniciando consulta para cédula: {args.cedula}")
        resultado = ejecutar_flujo(args.cedula, fecha_formateada, headless=args.headless)
        
        if resultado:
            storage.guardar(resultado)
            logger.info("Consulta completada exitosamente")
            print("\n" + "="*50)
            print("RESULTADO DE LA CONSULTA:")
            print("="*50)
            for key, value in resultado.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("="*50)
        else:
            logger.error("Consulta fallida")
    
    else:
        # Modo interactivo
        print("="*50)
        print("CONSULTA DE VIGENCIA DE CÉDULA")
        print("="*50)
        
        while True:
            cedula = input("\nIngrese el número de cédula (o 'salir' para terminar): ").strip()
            
            if cedula.lower() == 'salir':
                break
            
            if not validar_cedula(cedula):
                print("❌ Cédula inválida. Debe tener entre 6 y 10 dígitos.")
                continue
            
            fecha = input("Ingrese la fecha de expedición (DD/MM/YYYY) o presione Enter para omitir: ").strip()
            fecha_formateada = formatear_fecha(fecha) if fecha else None
            
            print(f"\nConsultando cédula: {cedula}...")
            resultado = ejecutar_flujo(cedula, fecha_formateada, headless=args.headless)
            
            if resultado:
                storage.guardar(resultado)
                print("\n✅ Consulta exitosa!")
                for key, value in resultado.items():
                    if value:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                print("\n❌ Consulta fallida. Revise los logs para más información.")
            
            continuar = input("\n¿Desea realizar otra consulta? (s/n): ").strip().lower()
            if continuar != 's':
                break

if __name__ == "__main__":
    main()