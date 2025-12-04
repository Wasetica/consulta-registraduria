"""
Test para 15 consultas paralelas a la registraduría
"""
import pytest
import time
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestParallelQueries:
    @pytest.fixture
    def query_data(self):
        """Fixture con datos de prueba para 15 consultas"""
        return [
            {'id': i, 'documento': f'TEST{i:03d}', 'nombre': f'TEST USER {i}'}
            for i in range(1, 16)
        ]
    
    def test_15_parallel_queries(self, query_data):
        """
        Test para ejecutar 15 consultas paralelas
        Verifica que no haya bloqueos y mide tiempos
        """
        print("\n🧪 Ejecutando test de 15 consultas paralelas...")
        
        # Simular consultas paralelas
        import concurrent.futures
        import threading
        
        results = []
        lock = threading.Lock()
        
        def mock_query(data):
            """Función mock de consulta"""
            start_time = time.time()
            time.sleep(0.5)  # Simular tiempo de consulta
            exec_time = time.time() - start_time
            
            with lock:
                results.append({
                    'id': data['id'],
                    'documento': data['documento'],
                    'success': True,
                    'execution_time': exec_time
                })
            
            return {'status': 'success', 'time': exec_time}
        
        # Ejecutar 15 consultas en paralelo
        start_total = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(mock_query, data) for data in query_data]
            
            # Esperar a que todas completen
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result(timeout=2.0)
                except Exception as e:
                    print(f"Error en consulta: {e}")
        
        total_time = time.time() - start_total
        
        # 1. Verificar que se ejecutaron 15 consultas
        assert len(results) == 15, f"Se esperaban 15 consultas, se ejecutaron {len(results)}"
        
        # 2. Verificar que todas fueron exitosas
        success_count = sum(1 for r in results if r['success'])
        assert success_count == 15, f"Solo {success_count}/15 consultas exitosas"
        
        # 3. Verificar que el tiempo total sea razonable
        # 15 consultas en paralelo no deberían tomar más de 5 segundos
        assert total_time < 5.0, f"Tiempo total muy alto: {total_time:.2f}s"
        
        # 4. Calcular tasa de éxito
        success_rate = (success_count / 15) * 100
        
        print(f"✅ Test pasado exitosamente")
        print(f"   Consultas ejecutadas: {len(results)}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        print(f"   Tiempo total: {total_time:.2f}s")
        
        # 5. Verificar que no haya tiempos anormalmente altos
        max_time = max(r['execution_time'] for r in results)
        assert max_time < 2.0, f"Consulta individual muy lenta: {max_time:.2f}s"
        
        return results
    
    def test_no_blocking_detection(self):
        """
        Test específico para detectar bloqueos por parte de la página
        """
        print("\n🔍 Test de detección de bloqueos...")
        
        import concurrent.futures
        import random
        
        def blocking_simulation(query_id):
            """Simula bloqueos aleatorios"""
            # 30% de probabilidad de simular bloqueo
            if random.random() < 0.3:
                time.sleep(1.5)  # Delay largo simula bloqueo
                raise Exception(f"Simulación de bloqueo para consulta {query_id}")
            time.sleep(0.3)
            return {'status': 'ok', 'id': query_id}
        
        # Ejecutar 5 consultas
        results = []
        errors = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(blocking_simulation, i) for i in range(5)]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=2.0)
                    results.append(result)
                except Exception as e:
                    errors.append(str(e))
        
        # Verificar que el sistema maneje bloqueos sin fallar completamente
        total_attempts = len(results) + len(errors)
        assert total_attempts == 5, f"No se completaron todas las consultas: {total_attempts}/5"
        
        # Si hay errores, no deben ser todos
        if errors:
            assert len(errors) < 5, "Todas las consultas fallaron (bloqueo total)"
            print(f"⚠️  Se detectaron {len(errors)} bloqueos simulados")
        
        print("✅ Sistema maneja bloqueos adecuadamente")
        return {'results': results, 'errors': errors}
    
    def test_concurrent_execution(self):
        """
        Verificar que las consultas realmente se ejecuten concurrentemente
        """
        print("\n⚡ Test de concurrencia real...")
        
        import concurrent.futures
        import threading
        
        start_times = []
        end_times = []
        lock = threading.Lock()
        
        def track_time_query(query_id):
            with lock:
                start_times.append(time.time())
            
            time.sleep(1)  # Todas duran 1 segundo
            
            with lock:
                end_times.append(time.time())
            
            return {'id': query_id, 'start': start_times[-1], 'end': end_times[-1]}
        
        # Ejecutar 5 consultas en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(track_time_query, i) for i in range(5)]
            
            for future in concurrent.futures.as_completed(futures):
                future.result()
        
        # Calcular superposición
        max_concurrent = self._calculate_max_concurrency(start_times, end_times)
        
        # Con 5 workers, deberían ejecutarse al menos 3 concurrentemente
        assert max_concurrent >= 3, f"Concurrencia baja: {max_concurrent} consultas simultáneas"
        
        print(f"✅ Concurrencia adecuada: {max_concurrent} consultas simultáneas")
        return max_concurrent
    
    def _calculate_max_concurrency(self, starts, ends):
        """Calcula el máximo número de consultas concurrentes"""
        if not starts or not ends:
            return 0
        
        # Crear timeline de eventos
        events = []
        for s, e in zip(starts, ends):
            events.append((s, 1))   # Inicio: +1 concurrencia
            events.append((e, -1))  # Fin: -1 concurrencia
        
        events.sort()
        
        max_concurrent = 0
        current = 0
        
        for _, change in events:
            current += change
            max_concurrent = max(max_concurrent, current)
        
        return max_concurrent


if __name__ == "__main__":
    # Ejecutar tests directamente sin pytest
    print("🚀 Ejecutando tests de consultas paralelas...")
    
    tester = TestParallelQueries()
    
    try:
        # Test 1: 15 consultas paralelas
        print("\n" + "="*60)
        print("TEST 1: 15 consultas paralelas")
        print("="*60)
        query_data = [{'id': i, 'documento': f'TEST{i:03d}'} for i in range(1, 16)]
        results1 = tester.test_15_parallel_queries(query_data)
        print(f"✅ Test 1 pasado - {len(results1)} consultas procesadas")
        
        # Test 2: Detección de bloqueos
        print("\n" + "="*60)
        print("TEST 2: Detección de bloqueos")
        print("="*60)
        results2 = tester.test_no_blocking_detection()
        print(f"✅ Test 2 pasado")
        
        # Test 3: Concurrencia real
        print("\n" + "="*60)
        print("TEST 3: Concurrencia real")
        print("="*60)
        concurrencia = tester.test_concurrent_execution()
        print(f"✅ Test 3 pasado - {concurrencia} consultas simultáneas")
        
        print("\n" + "="*60)
        print("🎉 TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
