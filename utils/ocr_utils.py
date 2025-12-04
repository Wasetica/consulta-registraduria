"""
Utilidades OCR para pruebas unitarias
"""
import re

def resolver_captcha(image_path=None):
    """
    Función mock para resolver CAPTCHAs en pruebas
    
    Args:
        image_path: Ruta a imagen del CAPTCHA (opcional en mock)
        
    Returns:
        Texto del CAPTCHA resuelto
    """
    # En pruebas, siempre retorna un valor fijo
    return "1234ABC"

def extraer_texto_imagen(image_path):
    """
    Extrae texto de una imagen (mock para pruebas)
    
    Args:
        image_path: Ruta a la imagen
        
    Returns:
        Texto extraído
    """
    # Simular extracción de texto
    if "cedula" in image_path.lower():
        return "CÉDULA: 123456789"
    elif "nombre" in image_path.lower():
        return "NOMBRE: JUAN PEREZ"
    else:
        return "TEXTO DE EJEMPLO PARA PRUEBAS"

def validar_texto_extraido(texto, patron=None):
    """
    Valida texto extraído por OCR
    
    Args:
        texto: Texto a validar
        patron: Patrón regex para validación
        
    Returns:
        Tuple (es_valido, mensaje)
    """
    if not texto or len(texto.strip()) < 3:
        return False, "Texto muy corto o vacío"
    
    if patron:
        if re.match(patron, texto):
            return True, "Texto válido según patrón"
        else:
            return False, "Texto no coincide con patrón"
    
    return True, "Texto válido"
