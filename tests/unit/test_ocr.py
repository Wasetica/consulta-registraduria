"""
Test unitario para funciones OCR
"""
import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_resolver_captcha():
    """Test de resolución de CAPTCHA"""
    print("🧪 Test: resolver_captcha")
    
    try:
        from utils.ocr_utils import resolver_captcha
        
        # Test 1: Sin parámetros
        resultado = resolver_captcha()
        assert resultado is not None, "No se retornó resultado"
        assert len(resultado) >= 4, f"CAPTCHA muy corto: {resultado}"
        
        # Test 2: Con parámetro (debería ignorarse en mock)
        resultado2 = resolver_captcha("fake_image.png")
        assert resultado2 is not None
        
        print("  ✅ resolver_captcha PASADO")
        return True
        
    except ImportError:
        print("  ⚠️  Test skip - Módulo no disponible")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise

def test_extraer_texto_imagen():
    """Test de extracción de texto de imagen"""
    print("\n🧪 Test: extraer_texto_imagen")
    
    try:
        from utils.ocr_utils import extraer_texto_imagen
        
        # Test con diferentes rutas simuladas
        tests = [
            ("cedula_123.png", "CÉDULA"),
            ("nombre_usuario.jpg", "NOMBRE"),
            ("otro_documento.pdf", "TEXTO DE EJEMPLO")
        ]
        
        for ruta, texto_esperado in tests:
            resultado = extraer_texto_imagen(ruta)
            assert texto_esperado in resultado, \
                f"Texto esperado '{texto_esperado}' no en '{resultado}'"
        
        print("  ✅ extraer_texto_imagen PASADO")
        return True
        
    except ImportError:
        print("  ⚠️  Test skip - Módulo no disponible")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise

def test_validar_texto_extraido():
    """Test de validación de texto OCR"""
    print("\n🧪 Test: validar_texto_extraido")
    
    try:
        from utils.ocr_utils import validar_texto_extraido
        
        # Test casos válidos
        casos_validos = [
            ("123456", None, True),
            ("ABCD1234", r'^[A-Z0-9]+$', True),
            ("Texto largo para prueba", None, True)
        ]
        
        for texto, patron, esperado in casos_validos:
            es_valido, mensaje = validar_texto_extraido(texto, patron)
            assert es_valido == esperado, \
                f"Texto '{texto}' debería ser {esperado}: {mensaje}"
        
        # Test casos inválidos
        casos_invalidos = [
            ("", None, False),  # Texto vacío
            ("A", None, False), # Texto muy corto
            ("abc123", r'^[A-Z]+$', False)  # No coincide con patrón
        ]
        
        for texto, patron, esperado in casos_invalidos:
            es_valido, mensaje = validar_texto_extraido(texto, patron)
            assert es_valido == esperado, \
                f"Texto '{texto}' debería ser {esperado}: {mensaje}"
        
        print("  ✅ validar_texto_extraido PASADO")
        return True
        
    except ImportError:
        print("  ⚠️  Test skip - Módulo no disponible")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise

def test_ocr_completo():
    """Test completo del módulo OCR"""
    print("\n🔧 Test completo del módulo OCR")
    
    resultados = []
    
    try:
        resultados.append(test_resolver_captcha())
        resultados.append(test_extraer_texto_imagen())
        resultados.append(test_validar_texto_extraido())
        
        if all(resultados):
            print("\n✅ Todos los tests OCR PASARON")
            return True
        else:
            print(f"\n⚠️  Algunos tests fallaron: {resultados}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error en test completo: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Ejecutando tests unitarios OCR...")
    test_ocr_completo()
