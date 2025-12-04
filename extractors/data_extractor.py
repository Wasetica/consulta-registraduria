"""
Sistema completo de extracción de datos de PDFs de registraduría
"""
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging

try:
    import pdfplumber
    import PyPDF2
    PDF_LIBS_AVAILABLE = True
except ImportError:
    PDF_LIBS_AVAILABLE = False
    print("⚠️  Instala: pip install pdfplumber PyPDF2")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegistraduriaPDFExtractor:
    """Extrae datos específicos de PDFs de la registraduría"""
    
    def __init__(self):
        # Patrones específicos para PDFs de registraduría colombiana
        self.patterns = {
            'nombre_completo': [
                r'Nombre[:\s]+([A-ZÑÁÉÍÓÚ\s]+?(?=\s{2,}|$))',
                r'NOMBRE[:\s]+([A-ZÑÁÉÍÓÚ\s]+?(?=\n|$))',
                r'Nombre del Ciudadano[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Ciudadano[:\s]+([A-ZÑÁÉÍÓÚ\s]+)'
            ],
            'documento': [
                r'Documento[:\s]+([\d\.]+)',
                r'C[ÉE]DULA[:\s]+([\d\.]+)',
                r'N[ÚU]MERO[:\s]+([\d\.]+)',
                r'Identificaci[ÓO]n[:\s]+([\d\.]+)',
                r'No\.?\s*([\d\.]+)'
            ],
            'fecha_expedicion': [
                r'Expedici[ÓO]n[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'Fecha Expedici[ÓO]n[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'Expedido[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'Expedición Documento[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
            ],
            'fecha_nacimiento': [
                r'Nacimiento[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'Fecha Nac\.?[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'Naci[ÓO] el[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
            ],
            'lugar_expedicion': [
                r'Lugar[:\s]+([A-ZÑÁÉÍÓÚ\s,]+?(?=\s{2,}|$))',
                r'Ciudad[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Municipio[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Expedido en[:\s]+([A-ZÑÁÉÍÓÚ\s]+)'
            ],
            'estado_vigencia': [
                r'Estado[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Vigencia[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Estado Civil[:\s]+([A-ZÑÁÉÍÓÚ\s]+)',
                r'Documento[:\s]+([A-ZÑÁÉÍÓÚ\s]+)'
            ],
            'direccion': [
                r'Direcci[ÓO]n[:\s]+([A-ZÑÁÉÍÓÚ0-9\s,.#-]+?(?=\s{2,}|$))',
                r'Reside en[:\s]+([A-ZÑÁÉÍÓÚ0-9\s,.#-]+)',
                r'Domicilio[:\s]+([A-ZÑÁÉÍÓÚ0-9\s,.#-]+)'
            ],
            'genero': [
                r'G[ÉE]NERO[:\s]+([A-ZÑÁÉÍÓÚ]+)',
                r'Sexo[:\s]+([A-ZÑÁÉÍÓÚ]+)',
                r'Género[:\s]+([A-ZÑÁÉÍÓÚ]+)'
            ],
            'rh': [
                r'Grupo Sangu[ií]neo[:\s]+([A-Z\+\-]+)',
                r'RH[:\s]+([A-Z\+\-]+)',
                r'Tipo de Sangre[:\s]+([A-Z\+\-]+)'
            ]
        }
        
        # Palabras clave para identificar PDF de registraduría
        self.keywords_registraduria = [
            'REGISTRADURÍA',
            'REGISTRADURIA',
            'ESTADO CIVIL',
            'IDENTIFICACIÓN',
            'CÉDULA DE CIUDADANÍA',
            'NUIP',
            'RNEC'
        ]
        
        logger.info("✅ Extractor de PDF inicializado")
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extrae datos de un PDF de registraduría
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            Diccionario con datos extraídos
        """
        if not PDF_LIBS_AVAILABLE:
            raise ImportError("Librerías PDF no disponibles. Instala pdfplumber y PyPDF2")
        
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF no encontrado: {pdf_path}")
        
        logger.info(f"📄 Extrayendo datos de: {pdf_path}")
        
        try:
            # Método 1: Usar pdfplumber (mejor para PDFs con texto)
            text = self._extract_with_pdfplumber(pdf_path)
            
            # Método 2: Si pdfplumber no obtiene texto, usar PyPDF2
            if not text or len(text.strip()) < 50:
                text = self._extract_with_pypdf2(pdf_path)
            
            # Verificar que sea un PDF de registraduría
            if not self._is_registraduria_pdf(text):
                logger.warning(f"⚠️  PDF puede no ser de registraduría: {pdf_path}")
            
            # Extraer datos
            datos_extraidos = self._extract_all_fields(text)
            
            # Validar extracción
            validacion = self._validate_extraction(datos_extraidos)
            
            # Añadir metadatos
            datos_extraidos['_metadata'] = {
                'pdf_path': pdf_path,
                'fecha_extraccion': datetime.now().isoformat(),
                'text_length': len(text),
                'validacion': validacion
            }
            
            logger.info(f"✅ Datos extraídos: {len(datos_extraidos)} campos")
            return datos_extraidos
            
        except Exception as e:
            logger.error(f"❌ Error extrayendo {pdf_path}: {e}")
            return {'error': str(e), 'pdf_path': pdf_path}
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extrae texto usando pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.warning(f"pdfplumber error: {e}")
            return ""
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extrae texto usando PyPDF2"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.warning(f"PyPDF2 error: {e}")
            return ""
    
    def _is_registraduria_pdf(self, text: str) -> bool:
        """Verifica si el texto parece ser de registraduría"""
        if not text:
            return False
        
        text_upper = text.upper()
        
        # Contar coincidencias con palabras clave
        matches = sum(1 for keyword in self.keywords_registraduria 
                     if keyword in text_upper)
        
        return matches >= 2  # Al menos 2 palabras clave
    
    def _extract_all_fields(self, text: str) -> Dict[str, Any]:
        """Extrae todos los campos del texto"""
        if not text:
            return {}
        
        # Limpiar y normalizar texto
        cleaned_text = self._clean_text(text)
        
        resultados = {}
        
        for campo, patrones in self.patterns.items():
            valor = self._extract_with_patterns(cleaned_text, patrones)
            if valor:
                # Post-procesamiento específico por campo
                if campo == 'documento':
                    valor = self._clean_documento(valor)
                elif campo in ['fecha_expedicion', 'fecha_nacimiento']:
                    valor = self._parse_fecha(valor)
                elif campo == 'nombre_completo':
                    valor = self._clean_nombre(valor)
                
                resultados[campo] = valor
        
        return resultados
    
    def _extract_with_patterns(self, text: str, patterns: List[str]) -> Optional[str]:
        """Intenta extraer usando múltiples patrones"""
        for pattern in patterns:
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    valor = match.group(1).strip()
                    if valor and valor not in ['N/A', 'NO APLICA', 'SIN INFORMACION']:
                        return valor
            except re.error as e:
                logger.warning(f"Error en patrón {pattern}: {e}")
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Limpia y prepara el texto para extracción"""
        # Unificar saltos de línea
        text = re.sub(r'\r\n', '\n', text)
        
        # Reemplazar múltiples espacios y saltos
        text = re.sub(r'\s+', ' ', text)
        
        # Unificar caracteres especiales
        replacements = {
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'Ñ': 'N', 'Ü': 'U',
            'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U',
            'ñ': 'N', 'ü': 'U'
        }
        
        for orig, repl in replacements.items():
            text = text.replace(orig, repl)
        
        return text.upper()
    
    def _clean_documento(self, documento: str) -> str:
        """Limpia número de documento"""
        # Remover puntos, espacios, guiones
        documento = re.sub(r'[\.\s\-]', '', documento)
        return documento
    
    def _clean_nombre(self, nombre: str) -> str:
        """Limpia y formatea nombre"""
        # Remover espacios múltiples
        nombre = re.sub(r'\s+', ' ', nombre).strip()
        
        # Capitalizar cada palabra
        palabras = nombre.split()
        palabras = [p.capitalize() for p in palabras]
        
        return ' '.join(palabras)
    
    def _parse_fecha(self, fecha_str: str) -> str:
        """Convierte fecha a formato YYYY-MM-DD"""
        try:
            # Intentar diferentes formatos
            formatos = [
                '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y',
                '%Y/%m/%d', '%Y-%m-%d'
            ]
            
            for formato in formatos:
                try:
                    fecha = datetime.strptime(fecha_str, formato)
                    return fecha.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # Si no coincide ningún formato, devolver original
            return fecha_str
            
        except Exception:
            return fecha_str
    
    def _validate_extraction(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los datos extraídos"""
        errores = []
        advertencias = []
        
        # Validar documento
        if 'documento' in datos:
            doc = datos['documento']
            if not (6 <= len(doc) <= 12):
                errores.append(f"Documento inválido: {doc}")
            elif not doc.isdigit():
                advertencias.append(f"Documento contiene caracteres no numéricos: {doc}")
        
        # Validar nombre
        if 'nombre_completo' in datos:
            nombre = datos['nombre_completo']
            if len(nombre) < 5:
                errores.append(f"Nombre muy corto: {nombre}")
            elif len(nombre.split()) < 2:
                advertencias.append(f"Nombre posiblemente incompleto: {nombre}")
        
        # Validar fechas
        for campo_fecha in ['fecha_expedicion', 'fecha_nacimiento']:
            if campo_fecha in datos:
                fecha = datos[campo_fecha]
                if not re.match(r'\d{4}-\d{2}-\d{2}', fecha):
                    advertencias.append(f"Formato de fecha no estándar en {campo_fecha}: {fecha}")
        
        return {
            'valido': len(errores) == 0,
            'errores': errores,
            'advertencias': advertencias,
            'campos_extraidos': list(datos.keys()),
            'total_campos': len(datos)
        }
    
    def batch_extract(self, pdf_folder: str, output_format: str = 'json') -> List[Dict]:
        """
        Extrae datos de múltiples PDFs
        
        Args:
            pdf_folder: Carpeta con PDFs
            output_format: 'json', 'csv', o 'all'
            
        Returns:
            Lista de resultados
        """
        folder_path = Path(pdf_folder)
        if not folder_path.exists():
            raise FileNotFoundError(f"Carpeta no encontrada: {pdf_folder}")
        
        resultados = []
        
        # Buscar archivos PDF
        pdf_files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.PDF"))
        
        logger.info(f"📂 Procesando {len(pdf_files)} PDFs de {pdf_folder}")
        
        for pdf_file in pdf_files:
            try:
                datos = self.extract_from_pdf(str(pdf_file))
                datos['archivo'] = pdf_file.name
                resultados.append(datos)
                
                logger.info(f"  ✅ {pdf_file.name}: {len(datos)} campos")
                
            except Exception as e:
                logger.error(f"  ❌ Error procesando {pdf_file.name}: {e}")
                resultados.append({
                    'archivo': pdf_file.name,
                    'error': str(e)
                })
        
        # Exportar resultados
        self._export_results(resultados, output_format, pdf_folder)
        
        return resultados
    
    def _export_results(self, resultados: List[Dict], format: str, folder: str):
        """Exporta resultados a diferentes formatos"""
        output_dir = Path(folder) / "extraidos"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format in ['json', 'all']:
            json_file = output_dir / f"datos_extraidos_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 JSON exportado: {json_file}")
        
        if format in ['csv', 'all']:
            # Convertir a CSV simple
            import csv
            
            # Obtener todos los campos únicos
            campos = set()
            for resultado in resultados:
                campos.update(resultado.keys())
            
            campos = sorted(campos)
            
            csv_file = output_dir / f"datos_extraidos_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                
                for resultado in resultados:
                    # Asegurar que todas las filas tengan todos los campos
                    row = {campo: resultado.get(campo, '') for campo in campos}
                    writer.writerow(row)
            
            logger.info(f"💾 CSV exportado: {csv_file}")


# Funciones de utilidad
def extract_and_save(pdf_path: str, output_json: str = None) -> Dict:
    """
    Función de conveniencia para extraer y guardar datos
    """
    extractor = RegistraduriaPDFExtractor()
    datos = extractor.extract_from_pdf(pdf_path)
    
    if output_json and 'error' not in datos:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"✅ Datos guardados en: {output_json}")
    
    return datos


# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Probando extractor de PDFs...")
    
    # Crear extractor
    extractor = RegistraduriaPDFExtractor()
    
    # Texto de ejemplo (simulando PDF de registraduría)
    texto_ejemplo = """
    REGISTRADURÍA NACIONAL DEL ESTADO CIVIL
    CERTIFICADO DE IDENTIFICACIÓN
    
    Nombre: JUAN CARLOS PEREZ GOMEZ
    Documento: 12.345.678.9
    Fecha Expedición: 15/01/2023
    Fecha Nacimiento: 20/05/1985
    Lugar Expedición: BOGOTÁ D.C.
    Estado: VIGENTE
    Dirección: CALLE 123 #45-67
    Género: MASCULINO
    Grupo Sanguíneo: O+
    
    Este documento es válido para todos los trámites.
    """
    
    # Probar extracción
    datos = extractor._extract_all_fields(texto_ejemplo)
    
    print("\n📋 Datos extraídos del ejemplo:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
    
    # Validar
    validacion = extractor._validate_extraction(datos)
    print(f"\n✅ Validación: {'VÁLIDO' if validacion['valido'] else 'INVÁLIDO'}")
    
    if validacion['errores']:
        print("Errores:", validacion['errores'])
    if validacion['advertencias']:
        print("Advertencias:", validacion['advertencias'])
    
    print("\n🎉 Extractor probado exitosamente!")
    print("\n📌 Para usar:")
    print("   1. extractor = RegistraduriaPDFExtractor()")
    print("   2. datos = extractor.extract_from_pdf('ruta/al/pdf.pdf')")
    print("   3. resultados = extractor.batch_extract('carpeta/pdf/')")
