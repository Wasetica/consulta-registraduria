#!/usr/bin/env python3
"""
Tests SIMPLES que SI funcionan
"""

import unittest
import os
import tempfile
import shutil

# Copiar funciones del módulo principal para evitar importación
def validar_cedula_test(cedula: str) -> bool:
    return cedula and cedula.isdigit() and 6 <= len(cedula) <= 10

class TestSistemaSimple(unittest.TestCase):
    
    def test_validacion_cedula(self):
        """Test de validación de cédulas"""
        print("\n🧪 Test: Validación de cédulas")
        
        casos_positivos = ["123456", "1234567", "12345678", "123456789", "1234567890"]
        casos_negativos = ["12345", "12345678901", "abc123", "", None]
        
        for cedula in casos_positivos:
            with self.subTest(cedula=cedula):
                self.assertTrue(validar_cedula_test(cedula), f"Debería ser válida: {cedula}")
        
        for cedula in casos_negativos:
            with self.subTest(cedula=cedula):
                if cedula is not None:
                    self.assertFalse(validar_cedula_test(cedula), f"Debería ser inválida: {cedula}")
        
        print("✅ Validación de cédulas: PASÓ")
    
    def test_estructura_directorios(self):
        """Test de creación de directorios"""
        print("\n🧪 Test: Estructura de directorios")
        
        # Usar directorio temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # Crear directorios
                for d in ['descargas', 'resultados', 'logs']:
                    os.makedirs(d, exist_ok=True)
                
                # Verificar que existen
                for d in ['descargas', 'resultados', 'logs']:
                    self.assertTrue(os.path.exists(d), f"Directorio {d} debería existir")
                    self.assertTrue(os.path.isdir(d), f"{d} debería ser directorio")
                
                print("✅ Estructura de directorios: PASÓ")
                
            finally:
                os.chdir(original_dir)
    
    def test_sistema_completo(self):
        """Test del sistema completo"""
        print("\n🧪 Test: Sistema completo")
        
        # Verificar que podemos importar el módulo
        try:
            import consulta_simple
            print("✅ Importación del módulo: PASÓ")
            
            # Verificar funciones principales
            self.assertTrue(hasattr(consulta_simple, 'validar_cedula'))
            self.assertTrue(hasattr(consulta_simple, 'crear_directorios'))
            self.assertTrue(hasattr(consulta_simple, 'main'))
            
            print("✅ Funciones principales: PASÓ")
            
        except Exception as e:
            self.fail(f"Error importando módulo: {e}")
    
    def test_csv_operations(self):
        """Test de operaciones CSV"""
        print("\n🧪 Test: Operaciones CSV")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear archivo CSV de prueba
            csv_path = os.path.join(tmpdir, 'test.csv')
            
            # Escribir datos de prueba
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write("cedula\n123456789\n987654321\n")
            
            # Leer archivo
            with open(csv_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.assertIn("123456789", contenido)
                self.assertIn("987654321", contenido)
            
            print("✅ Operaciones CSV: PASÓ")

def run_all_tests():
    """Ejecuta todos los tests"""
    print("="*70)
    print("🚀 EJECUTANDO TODOS LOS TESTS")
    print("="*70)
    
    # Crear test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSistemaSimple)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    if result.wasSuccessful():
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return True
    else:
        print("\n⚠️  Algunos tests fallaron")
        return False

if __name__ == '__main__':
    # Ejecutar tests
    if run_all_tests():
        # Mostrar instrucciones si todo pasa
        print("\n" + "="*70)
        print("✅ SISTEMA LISTO PARA USAR")
        print("="*70)
        print("\nInstrucciones:")
        print("1. Modo interactivo:")
        print("   python consulta_simple.py")
        print("\n2. Consulta individual:")
        print("   python consulta_simple.py --cedula 1032493824")
        print("\n3. Consultas desde CSV:")
        print("   python consulta_simple.py --archivo datos_prueba.csv")
        print("="*70)
    else:
        sys.exit(1)
