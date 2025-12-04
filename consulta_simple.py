#!/usr/bin/env python3
"""
CONSULTA REAL A REGISTRADURÍA NACIONAL
Conecta REALMENTE a: https://certvigenciacedula.registraduria.gov.co/Datos.aspx
Descarga PDFs reales y extrae información
"""
import os
import sys
import time
import csv
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/consulta_real.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear directorios
Path("descargas").mkdir(exist_ok=True)
Path("resultados").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

class RegistraduriaScraper:
    """Scraper REAL para la página de la Registraduría"""
    
    def __init__(self, headless: bool = True):
        """
        Inicializa el scraper
        
        Args:
            headless: Si es True, navegador sin interfaz gráfica
        """
        self.headless = headless
        self.browser = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"✅ Scraper inicializado (Session: {self.session_id})")
    
    def iniciar_navegador(self):
        """Inicia el navegador Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            
            logger.info("🚀 Iniciando navegador Chrome...")
            
            # Configurar opciones de Chrome
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Iniciar driver
            service = Service(ChromeDriverManager().install())
            self.browser = webdriver.Chrome(service=service, options=chrome_options)
            
            # Configurar tiempo de espera
            self.wait = WebDriverWait(self.browser, 30)
            
            logger.info("✅ Navegador iniciado exitosamente")
            return True
            
        except ImportError as e:
            logger.error(f"❌ Dependencias faltantes: {e}")
            logger.info("📦 Instala: pip install selenium webdriver-manager")
            return False
        except Exception as e:
            logger.error(f"❌ Error iniciando navegador: {e}")
            return False
    
    def resolver_captcha(self):
        """Resuelve CAPTCHA de la página"""
        try:
            from PIL import Image
            import pytesseract
            import io
            import base64
            
            logger.info("🔍 Buscando CAPTCHA...")
            
            # Esperar a que aparezca el CAPTCHA
            captcha_img = self.wait.until(
                EC.presence_of_element_located((By.ID, "imgCaptcha"))
            )
            
            # Tomar screenshot del CAPTCHA
            captcha_screenshot = captcha_img.screenshot_as_png
            
            # Usar pytesseract para leer el CAPTCHA
            image = Image.open(io.BytesIO(captcha_screenshot))
            
            # Procesar imagen para mejor OCR
            image = image.convert('L')  # Escala de grises
            image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Binarizar
            
            # Leer texto
            captcha_text = pytesseract.image_to_string(image).strip()
            
            # Limpiar texto
            captcha_text = re.sub(r'[^A-Z0-9]', '', captcha_text)
            
            if len(captcha_text) >= 4:
                logger.info(f"✅ CAPTCHA resuelto: {captcha_text}")
                return captcha_text
            else:
                logger.warning("⚠️  CAPTCHA no legible, usando valor por defecto")
                return "ABCD"  # Valor por defecto para pruebas
                
        except ImportError:
            logger.warning("⚠️  pytesseract no instalado, usando CAPTCHA simulado")
            return "1234"
        except Exception as e:
            logger.warning(f"⚠️  Error resolviendo CAPTCHA: {e}, usando simulado")
            return "TEST"
    
    def consultar_cedula(self, cedula: str, fecha_expedicion: str = None):
        """
        Consulta REAL una cédula en la Registraduría
        
        Args:
            cedula: Número de cédula a consultar
            fecha_expedicion: Fecha en formato DD/MM/YYYY (opcional)
            
        Returns:
            Diccionario con resultados
        """
        inicio = time.time()
        logger.info(f"🔍 Consultando cédula REAL: {cedula}")
        
        try:
            # 1. Navegar a la página
            url = "https://certvigenciacedula.registraduria.gov.co/Datos.aspx"
            logger.info(f"🌐 Navegando a: {url}")
            self.browser.get(url)
            
            # 2. Esperar a que cargue la página
            self.wait.until(
                EC.presence_of_element_located((By.ID, "txtNumeroDocumento"))
            )
            logger.info("✅ Página cargada")
            
            # 3. Llenar formulario
            # Número de documento
            input_doc = self.browser.find_element(By.ID, "txtNumeroDocumento")
            input_doc.clear()
            input_doc.send_keys(cedula)
            
            # Fecha de expedición (si se proporciona)
            if fecha_expedicion:
                try:
                    input_fecha = self.browser.find_element(By.ID, "txtFechaExpedicion")
                    input_fecha.clear()
                    input_fecha.send_keys(fecha_expedicion)
                    logger.info(f"📅 Fecha ingresada: {fecha_expedicion}")
                except:
                    logger.warning("⚠️  No se pudo ingresar fecha")
            
            # 4. Resolver CAPTCHA
            captcha_text = self.resolver_captcha()
            input_captcha = self.browser.find_element(By.ID, "txtCaptcha")
            input_captcha.clear()
            input_captcha.send_keys(captcha_text)
            
            # 5. Enviar formulario
            btn_consultar = self.browser.find_element(By.ID, "btnConsultar")
            btn_consultar.click()
            logger.info("📤 Formulario enviado")
            
            # 6. Esperar resultado (PDF o mensaje de error)
            time.sleep(3)  # Esperar a que procese
            
            # 7. Verificar si hay PDF
            pdf_descargado = self._descargar_pdf(cedula)
            
            # 8. Extraer información si se descargó PDF
            datos = {}
            if pdf_descargado:
                datos = self._extraer_datos_pdf(pdf_descargado)
            
            tiempo_total = time.time() - inicio
            
            resultado = {
                'cedula': cedula,
                'fecha_expedicion': fecha_expedicion,
                'consulta_exitosa': pdf_descargado is not None,
                'tiempo_respuesta': round(tiempo_total, 2),
                'fecha_consulta': datetime.now().isoformat(),
                'pdf_descargado': pdf_descargado,
                'datos_extraidos': datos,
                'error': None if pdf_descargado else 'No se pudo descargar PDF'
            }
            
            logger.info(f"✅ Consulta completada en {tiempo_total:.2f}s")
            return resultado
            
        except Exception as e:
            tiempo_total = time.time() - inicio
            logger.error(f"❌ Error en consulta: {e}")
            
            return {
                'cedula': cedula,
                'consulta_exitosa': False,
                'tiempo_respuesta': round(tiempo_total, 2),
                'fecha_consulta': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _descargar_pdf(self, cedula: str) -> Optional[str]:
        """Intenta descargar el PDF generado"""
        try:
            # Buscar enlace o iframe del PDF
            pdf_url = None
            
            # Opción 1: Buscar iframe con PDF
            iframes = self.browser.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                src = iframe.get_attribute("src")
                if src and ".pdf" in src.lower():
                    pdf_url = src
                    break
            
            # Opción 2: Buscar enlace directo
            if not pdf_url:
                links = self.browser.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and ".pdf" in href.lower():
                        pdf_url = href
                        break
            
            if pdf_url:
                logger.info(f"📄 PDF encontrado: {pdf_url}")
                
                # Descargar usando requests
                import requests
                
                # Obtener cookies del navegador
                cookies = self.browser.get_cookies()
                session = requests.Session()
                
                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
                
                # Descargar PDF
                response = session.get(pdf_url, stream=True)
                
                if response.status_code == 200:
                    # Guardar PDF
                    pdf_path = Path("descargas") / f"cedula_{cedula}_{self.session_id}.pdf"
                    
                    with open(pdf_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    logger.info(f"✅ PDF descargado: {pdf_path} ({pdf_path.stat().st_size/1024:.1f} KB)")
                    return str(pdf_path)
                
            logger.warning("⚠️  No se encontró PDF para descargar")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error descargando PDF: {e}")
            return None
    
    def _extraer_datos_pdf(self, pdf_path: str) -> Dict:
        """Extrae datos del PDF descargado"""
        try:
            import PyPDF2
            
            texto = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    texto += page.extract_text()
            
            # Extraer información usando regex
            datos = {}
            
            # Patrones para la Registraduría
            patrones = {
                'nombre': r'Nombre[:\s]+([A-Z\sÁÉÍÓÚÑ]+)',
                'documento': r'Documento[:\s]+([\d\.]+)',
                'fecha_expedicion': r'Fecha Expedici[Óo]n[:\s]+(\d{2}/\d{2}/\d{4})',
                'fecha_nacimiento': r'Nacimiento[:\s]+(\d{2}/\d{2}/\d{4})',
                'lugar_expedicion': r'Lugar[:\s]+([A-Z\sÁÉÍÓÚÑ\.]+)',
                'estado': r'Estado[:\s]+([A-Z\s]+)',
                'direccion': r'Direcci[Óo]n[:\s]+([A-Z0-9\s\-#\.]+)'
            }
            
            for campo, patron in patrones.items():
                match = re.search(patron, texto, re.IGNORECASE)
                if match:
                    datos[campo] = match.group(1).strip()
            
            logger.info(f"📋 {len(datos)} campos extraídos del PDF")
            return datos
            
        except ImportError:
            logger.warning("⚠️  PyPDF2 no instalado, no se pueden extraer datos")
            return {'error': 'PyPDF2 no instalado'}
        except Exception as e:
            logger.error(f"❌ Error extrayendo datos PDF: {e}")
            return {'error': str(e)}
    
    def cerrar(self):
        """Cierra el navegador"""
        if self.browser:
            self.browser.quit()
            logger.info("👋 Navegador cerrado")

def consulta_individual(cedula: str, fecha: str = None):
    """Consulta individual con scraper real"""
    scraper = None
    try:
        scraper = RegistraduriaScraper(headless=True)
        
        if scraper.iniciar_navegador():
            resultado = scraper.consultar_cedula(cedula, fecha)
            return resultado
        else:
            return {
                'cedula': cedula,
                'consulta_exitosa': False,
                'error': 'No se pudo iniciar navegador'
            }
            
    except Exception as e:
        return {
            'cedula': cedula,
            'consulta_exitosa': False,
            'error': str(e)
        }
    finally:
        if scraper:
            scraper.cerrar()

def guardar_resultado_csv(resultado: dict, archivo: str = "resultados_reales.csv"):
    """Guarda resultado en CSV"""
    try:
        archivo_path = Path("resultados") / archivo
        
        # Preparar datos para CSV
        datos_csv = {
            'cedula': resultado.get('cedula'),
            'fecha_expedicion': resultado.get('fecha_expedicion'),
            'consulta_exitosa': resultado.get('consulta_exitosa', False),
            'tiempo_respuesta': resultado.get('tiempo_respuesta', 0),
            'fecha_consulta': resultado.get('fecha_consulta'),
            'pdf_descargado': resultado.get('pdf_descargado'),
            'error': resultado.get('error')
        }
        
        # Agregar datos extraídos
        datos_extraidos = resultado.get('datos_extraidos', {})
        for key, value in datos_extraidos.items():
            datos_csv[f'dato_{key}'] = value
        
        campos = list(datos_csv.keys())
        existe = archivo_path.exists()
        
        with open(archivo_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            if not existe:
                writer.writeheader()
            writer.writerow(datos_csv)
        
        print(f"✅ Resultado guardado en: {archivo_path}")
        return archivo_path
        
    except Exception as e:
        print(f"❌ Error guardando: {e}")
        return None

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Consulta REAL a Registraduría Nacional',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos REALES:
  %(prog)s --cedula 1032493824 --fecha 09/10/2015
  %(prog)s --archivo cedulas.csv
  %(prog)s --test-paralelo  # Prueba con 15 documentos
        """
    )
    
    parser.add_argument('--cedula', '-c', type=str, help='Número de cédula a consultar')
    parser.add_argument('--fecha', '-f', type=str, help='Fecha expedición (DD/MM/YYYY)')
    parser.add_argument('--archivo', '-a', type=str, help='Archivo CSV con cédulas')
    parser.add_argument('--test-paralelo', action='store_true', help='Prueba 15 consultas paralelas')
    parser.add_argument('--headless', action='store_true', default=True, help='Navegador sin interfaz')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🔍 CONSULTA REAL - REGISTRADURÍA NACIONAL")
    print("URL: https://certvigenciacedula.registraduria.gov.co/Datos.aspx")
    print("="*60)
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    try:
        import selenium
        import webdriver_manager
        print("✅ Selenium instalado")
    except ImportError:
        print("❌ Faltan dependencias. Instala:")
        print("   pip install selenium webdriver-manager pytesseract Pillow PyPDF2")
        return
    
    if args.cedula:
        # Consulta individual
        print(f"\n📄 Consultando cédula: {args.cedula}")
        if args.fecha:
            print(f"📅 Con fecha: {args.fecha}")
        
        resultado = consulta_individual(args.cedula, args.fecha)
        
        print(f"\n📊 RESULTADO:")
        print(f"  ✅ Consulta exitosa: {resultado.get('consulta_exitosa', False)}")
        print(f"  ⏱️  Tiempo respuesta: {resultado.get('tiempo_respuesta', 0)}s")
        
        if resultado.get('pdf_descargado'):
            print(f"  📄 PDF descargado: {resultado['pdf_descargado']}")
        
        if resultado.get('datos_extraidos'):
            print(f"  📋 Datos extraídos:")
            for key, value in resultado['datos_extraidos'].items():
                if value and key != 'error':
                    print(f"    • {key}: {value}")
        
        # Guardar resultado
        archivo_csv = guardar_resultado_csv(resultado)
        
    elif args.archivo:
        # Consultas desde archivo
        print(f"\n📁 Procesando archivo: {args.archivo}")
        
        if not Path(args.archivo).exists():
            print(f"❌ Archivo no encontrado: {args.archivo}")
            return
        
        # Leer cédulas del archivo
        cedulas = []
        try:
            with open(args.archivo, 'r') as f:
                for linea in f:
                    cedula = linea.strip()
                    if cedula and cedula.isdigit():
                        cedulas.append(cedula)
            
            print(f"📋 {len(cedulas)} cédulas encontradas")
            
            # Procesar en serie (para paralelo usar main_final.py)
            for i, cedula in enumerate(cedulas[:10], 1):  # Limitar a 10
                print(f"\n[{i}/{min(10, len(cedulas))}] Consultando: {cedula}")
                resultado = consulta_individual(cedula)
                
                if resultado.get('consulta_exitosa'):
                    print(f"  ✅ Éxito")
                else:
                    print(f"  ❌ Error: {resultado.get('error', 'Desconocido')}")
                
                guardar_resultado_csv(resultado)
                time.sleep(2)  # Esperar entre consultas
        
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
    
    elif args.test_paralelo:
        # Prueba con 15 consultas paralelas
        print("\n⚡ EJECUTANDO 15 CONSULTAS PARALELAS (REAL)")
        print("⚠️  Esta prueba REAL puede tomar varios minutos")
        
        # Usar el sistema completo que ya tienes
        if Path("main_final.py").exists():
            print("🚀 Usando sistema completo...")
            os.system("python main_final.py --test-paralelo")
        else:
            print("❌ main_final.py no encontrado")
            print("ℹ️  Ejecuta: python -m pytest tests/parallel/test_concurrent_queries.py -v")
    
    else:
        # Modo interactivo
        print("\n🔧 MODO INTERACTIVO")
        print("="*40)
        
        cedula = input("Ingrese número de cédula: ").strip()
        if not cedula or not cedula.isdigit():
            print("❌ Cédula inválida")
            return
        
        fecha = input("Fecha expedición (DD/MM/YYYY, opcional): ").strip()
        if fecha and not re.match(r'\d{2}/\d{2}/\d{4}', fecha):
            print("⚠️  Formato fecha inválido, usando sin fecha")
            fecha = None
        
        print(f"\n🔍 Consultando: {cedula}...")
        resultado = consulta_individual(cedula, fecha)
        
        print(f"\n📊 RESULTADO:")
        for key, value in resultado.items():
            if key not in ['datos_extraidos', 'error'] and value:
                print(f"  {key}: {value}")
        
        if resultado.get('consulta_exitosa'):
            print("🎉 ¡Consulta REAL exitosa!")
        else:
            print("⚠️  Consulta fallida, revisa logs/consulta_real.log")

if __name__ == "__main__":
    try:
        main()
        print("\n🎉 Proceso completado")
        print("📁 Revisa: descargas/, resultados/, logs/")
    except KeyboardInterrupt:
        print("\n⏹️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
