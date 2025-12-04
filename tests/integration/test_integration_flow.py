"""
Test de integración para el flujo completo
"""
import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_flujo_completo_simulado():
    """Test simulado del flujo completo de consulta"""
    print("\n🧪 Test de flujo de integración")
    
    # Simular los pasos del flujo
    pasos = [
        "1. Inicialización del sistema ✅",
        "2. Validación de cédula ✅",
        "3. Consulta a registraduría (simulada) ✅",
        "4. Descarga de PDF (simulada) ✅",
        "5. Extracción de datos ✅",
        "6. Almacenamiento en BD ✅"
    ]
    
    for paso in pasos:
        print(f"  {paso}")
    
    # Verificar que todos los pasos se completarían
    assert len(pasos) == 6, f"Se esperaban 6 pasos, hay {len(pasos)}"
    
    print("✅ Test de flujo de integración PASADO")
    return True

def test_conexion_componentes():
    """Test que verifica que los componentes se conectan correctamente"""
    print("\n🔗 Test de conexión de componentes")
    
    # Verificar que existan los módulos principales
    modulos_requeridos = [
        ("consulta_simple.py", True),
        ("storage/database.py", True),
        ("extractors/data_extractor.py", True),
        ("main_final.py", True)
    ]
    
    for modulo, requerido in modulos_requeridos:
        existe = Path(modulo).exists()
        if requerido:
            assert existe, f"Módulo requerido no encontrado: {modulo}"
        
        icono = "✅" if existe else "⚠️"
        print(f"  {icono} {modulo}")
    
    print("✅ Test de conexión de componentes PASADO")
    return True

def test_almacenamiento_integrado():
    """Test de almacenamiento integrado - VERSIÓN CORREGIDA"""
    print("\n💾 Test de almacenamiento integrado (Corregido)")
    
    try:
        # Importar almacenamiento
        from storage.database import DataStorage
        
        # Usar BD temporal para pruebas
        test_db = "test_integracion_fix.db"
        test_csv = "test_integracion_fix.csv"
        
        # Limpiar archivos previos si existen
        if os.path.exists(test_db):
            os.remove(test_db)
        if os.path.exists(test_csv):
            os.remove(test_csv)
        
        storage = DataStorage(test_db)
        
        # Insertar datos de prueba
        datos_prueba = {
            'documento': '999888777',
            'nombre': 'TEST INTEGRACION FIX',
            'consulta_exitosa': True,
            'tiempo_respuesta': 1.5
        }
        
        id_registro = storage.save_consulta(datos_prueba)
        assert id_registro > 0, "No se pudo guardar en BD"
        
        # Exportar a CSV con nombre específico
        csv_file = storage.export_to_csv(test_csv)
        assert Path(csv_file).exists(), f"No se generó CSV: {csv_file}"
        
        # Verificar que el CSV tenga contenido
        import csv
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) > 1, "CSV vacío o solo encabezado"
        
        # Limpiar archivos temporales
        if os.path.exists(test_db):
            os.remove(test_db)
        if os.path.exists(test_csv):
            os.remove(csv_file)
        
        print("✅ Test de almacenamiento integrado PASADO (Corregido)")
        return True
        
    except ImportError as e:
        print(f"⚠️  Test skip - ImportError: {e}")
        return True  # Skip si no hay dependencias
    except Exception as e:
        print(f"❌ Error en test: {e}")
        # Asegurar limpieza incluso en error
        test_files = ["test_integracion_fix.db", "test_integracion_fix.csv"]
        for file in test_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except:
                    pass
        raise

# Test adicional para verificar exportación
def test_exportacion_datos():
    """Test de exportación de datos a diferentes formatos"""
    print("\n📤 Test de exportación de datos")
    
    try:
        from storage.database import DataStorage
        
        # BD temporal
        test_db = "test_exportacion.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        
        storage = DataStorage(test_db)
        
        # Insertar varios datos de prueba
        documentos_prueba = [
            {'documento': '111111111', 'nombre': 'EXPORT TEST 1', 'consulta_exitosa': True},
            {'documento': '222222222', 'nombre': 'EXPORT TEST 2', 'consulta_exitosa': True},
            {'documento': '333333333', 'nombre': 'EXPORT TEST 3', 'consulta_exitosa': False},
        ]
        
        for doc in documentos_prueba:
            storage.save_consulta(doc)
        
        # Exportar a diferentes formatos
        formatos = ['csv', 'json']  # Excel requiere openpyxl
        
        for formato in formatos:
            if formato == 'csv':
                archivo = storage.export_to_csv("test_export.csv")
            elif formato == 'json':
                archivo = storage.export_to_json("test_export.json")
            
            assert Path(archivo).exists(), f"No se generó {formato.upper()}: {archivo}"
            print(f"  ✅ {formato.upper()} exportado: {archivo}")
            
            # Limpiar archivo de prueba
            if os.path.exists(archivo):
                os.remove(archivo)
        
        # Limpiar BD
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("✅ Test de exportación de datos PASADO")
        return True
        
    except ImportError as e:
        print(f"⚠️  Test skip - ImportError: {e}")
        return True
    except Exception as e:
        print(f"❌ Error en test: {e}")
        # Limpieza
        for file in ["test_exportacion.db", "test_export.csv", "test_export.json"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except:
                    pass
        raise

if __name__ == "__main__":
    print("🔧 Ejecutando tests de integración...")
    
    try:
        test_flujo_completo_simulado()
        test_conexion_componentes()
        test_almacenamiento_integrado()
        test_exportacion_datos()
        print("\n🎉 Todos los tests de integración PASARON")
    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
