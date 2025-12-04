"""
Integrador del sistema de consultas paralelas con consulta_simple.py
"""
import sys
import os
from pathlib import Path
import importlib.util
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsultaSimpleIntegrator:
    """Integra el sistema de consultas paralelas con consulta_simple.py"""
    
    def __init__(self):
        self.consulta_module = None
        self.consulta_func = None
        self._load_consulta_simple()
    
    def _load_consulta_simple(self):
        """Intenta cargar el módulo consulta_simple.py"""
        try:
            # Agregar directorio actual al path
            sys.path.insert(0, str(Path.cwd()))
            
            # Intentar importar directamente
            import consulta_simple
            self.consulta_module = consulta_simple
            
            # Buscar función principal de consulta
            if hasattr(consulta_simple, 'realizar_consulta'):
                self.consulta_func = consulta_simple.realizar_consulta
            elif hasattr(consulta_simple, 'consultar_documento'):
                self.consulta_func = consulta_simple.consultar_documento
            elif hasattr(consulta_simple, 'main'):
                self.consulta_func = consulta_simple.main
            else:
                # Buscar cualquier función que tenga 'consulta' en el nombre
                for attr_name in dir(consulta_simple):
                    if 'consulta' in attr_name.lower() and callable(getattr(consulta_simple, attr_name)):
                        self.consulta_func = getattr(consulta_simple, attr_name)
                        break
            
            if self.consulta_func:
                logger.info(f"✅ Módulo consulta_simple cargado. Función: {self.consulta_func.__name__}")
            else:
                logger.warning("⚠️  Módulo cargado pero no se encontró función de consulta")
                
        except ImportError as e:
            logger.error(f"❌ No se pudo importar consulta_simple: {e}")
            self._create_mock_consulta()
    
    def _create_mock_consulta(self):
        """Crea una función mock si no existe consulta_simple"""
        logger.info("📝 Creando función mock para pruebas...")
        
        import time
        import random
        
        def mock_consulta(documento: str):
            """Función mock que simula consulta a registraduría"""
            logger.debug(f"🔍 Mock consultando documento: {documento}")
            
            # Simular tiempo de procesamiento
            tiempo = random.uniform(0.5, 2.0)
            time.sleep(tiempo)
            
            # Simular éxito/error aleatorio
            if random.random() < 0.85:  # 85% de éxito
                return {
                    'success': True,
                    'documento': documento,
                    'nombre': f'CIUDADANO MOCK {documento}',
                    'fecha_expedicion': '2023-01-15',
                    'estado_vigencia': 'VIGENTE',
                    'tiempo_respuesta': tiempo,
                    'fuente': 'MOCK'
                }
            else:
                raise Exception(f"Error simulado en consulta de {documento}")
        
        self.consulta_func = mock_consulta
        logger.info("✅ Función mock creada para pruebas")
    
    def realizar_consulta(self, documento: str, **kwargs):
        """
        Realiza una consulta usando consulta_simple o mock
        
        Args:
            documento: Número de documento a consultar
            **kwargs: Argumentos adicionales para la función
            
        Returns:
            Resultado de la consulta
        """
        if not self.consulta_func:
            raise RuntimeError("No hay función de consulta disponible")
        
        try:
            # Intentar llamar a la función con diferentes firmas
            import inspect
            sig = inspect.signature(self.consulta_func)
            
            if 'documento' in sig.parameters:
                return self.consulta_func(documento=documento, **kwargs)
            elif len(sig.parameters) >= 1:
                return self.consulta_func(documento, **kwargs)
            else:
                return self.consulta_func()
                
        except Exception as e:
            logger.error(f"❌ Error en consulta para {documento}: {e}")
            raise
    
    def test_integracion(self, documentos: list = None):
        """Prueba la integración con consultas reales/mock"""
        if documentos is None:
            documentos = ['123456789', '987654321', '112233445']
        
        print("\n" + "="*60)
        print("🧪 TEST DE INTEGRACIÓN CON CONSULTA_SIMPLE")
        print("="*60)
        
        resultados = []
        
        for doc in documentos:
            try:
                print(f"🔍 Consultando: {doc}...")
                resultado = self.realizar_consulta(doc)
                
                if resultado and resultado.get('success', False):
                    print(f"  ✅ Éxito: {resultado.get('nombre', 'N/A')}")
                    resultados.append({
                        'documento': doc,
                        'estado': 'EXITOSA',
                        'datos': resultado
                    })
                else:
                    print(f"  ❌ Fallo: {resultado.get('error', 'Error desconocido')}")
                    resultados.append({
                        'documento': doc,
                        'estado': 'FALLIDA',
                        'error': str(resultado.get('error', 'Error desconocido'))
                    })
                    
            except Exception as e:
                print(f"  💥 Error: {e}")
                resultados.append({
                    'documento': doc,
                    'estado': 'ERROR',
                    'error': str(e)
                })
        
        # Resumen
        exitosas = sum(1 for r in resultados if r['estado'] == 'EXITOSA')
        total = len(resultados)
        
        print("\n" + "="*60)
        print("📊 RESULTADOS DE INTEGRACIÓN")
        print("="*60)
        print(f"Total consultas: {total}")
        print(f"Exitosas: {exitosas}")
        print(f"Fallidas/Errores: {total - exitosas}")
        print(f"Tasa éxito: {(exitosas/total*100):.1f}%")
        
        if exitosas == total:
            print("✅ Integración EXITOSA")
        elif exitosas >= total * 0.7:
            print("⚠️  Integración PARCIAL (revisar fallos)")
        else:
            print("❌ Integración con PROBLEMAS")
        
        return resultados


# Integración con sistema paralelo
def crear_funcion_para_paralelo(integrator: ConsultaSimpleIntegrator):
    """
    Crea una función compatible con el sistema de consultas paralelas
    
    Returns:
        Función que toma {'documento': '123'} y retorna resultado
    """
    def funcion_para_sistema_paralelo(query_data: dict):
        """
        Función wrapper para el sistema paralelo
        
        Args:
            query_data: Dict con al menos {'documento': '123456789'}
            
        Returns:
            Resultado formateado para sistema paralelo
        """
        import time
        
        documento = query_data.get('documento')
        if not documento:
            raise ValueError("query_data debe contener 'documento'")
        
        inicio = time.time()
        
        try:
            # Realizar consulta
            resultado = integrator.realizar_consulta(documento)
            
            # Formatear para sistema paralelo
            tiempo_total = time.time() - inicio
            
            return {
                'success': resultado.get('success', True),
                'documento': documento,
                'nombre': resultado.get('nombre', ''),
                'tiempo_respuesta': tiempo_total,
                'datos_completos': resultado,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            tiempo_total = time.time() - inicio
            return {
                'success': False,
                'documento': documento,
                'error': str(e),
                'tiempo_respuesta': tiempo_total,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    return funcion_para_sistema_paralelo


# Script principal para probar integración
if __name__ == "__main__":
    print("🔗 INTEGRADOR CON CONSULTA_SIMPLE.PY")
    print("="*60)
    
    # Crear integrador
    integrator = ConsultaSimpleIntegrator()
    
    # Probar integración
    documentos_prueba = ['100000001', '100000002', '100000003', '100000004', '100000005']
    resultados = integrator.test_integracion(documentos_prueba)
    
    # Crear función para sistema paralelo
    funcion_paralelo = crear_funcion_para_paralelo(integrator)
    
    print("\n🔧 Función para sistema paralelo creada:")
    print("   funcion_paralelo({'documento': '123456789'})")
    
    # Probar función paralelo
    print("\n🧪 Probando función para sistema paralelo...")
    try:
        test_result = funcion_paralelo({'documento': '999999999', 'id': 1})
        print(f"  ✅ Test exitoso: {test_result.get('success', False)}")
        if test_result.get('success'):
            print(f"  📋 Nombre: {test_result.get('nombre')}")
            print(f"  ⏱️  Tiempo: {test_result.get('tiempo_respuesta'):.2f}s")
    except Exception as e:
        print(f"  ❌ Error en test: {e}")
    
    print("\n" + "="*60)
    print("📌 INSTRUCCIONES PARA USAR EN TESTS PARALELOS:")
    print("="*60)
    print("""
# En tu test_concurrent_queries.py, agrega:

from integrador_consulta_simple import (
    ConsultaSimpleIntegrator, 
    crear_funcion_para_paralelo
)

# Crear integrador y función
integrator = ConsultaSimpleIntegrator()
funcion_consulta_real = crear_funcion_para_paralelo(integrator)

# Usar en lugar de mock_query_func
results = executor.execute_parallel_queries(funcion_consulta_real, query_data)
    """)
    
    print("\n🎉 Integrador listo para usar!")
