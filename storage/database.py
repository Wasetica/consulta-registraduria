"""
Sistema completo de almacenamiento para consultas de registraduría
"""
import sqlite3
import json
import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStorage:
    """Clase principal para almacenamiento de datos"""
    
    def __init__(self, db_name: str = "consultas_registraduria.db"):
        self.db_name = db_name
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.init_database()
        logger.info(f"✅ Sistema de almacenamiento inicializado: {db_name}")
    
    def init_database(self) -> None:
        """Inicializa la base de datos SQLite con todas las tablas necesarias"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla principal de consultas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                documento TEXT NOT NULL,
                nombre TEXT,
                fecha_expedicion TEXT,
                fecha_nacimiento TEXT,
                lugar_expedicion TEXT,
                estado_vigencia TEXT,
                direccion TEXT,
                pdf_path TEXT,
                consulta_exitosa BOOLEAN DEFAULT 0,
                tiempo_respuesta REAL,
                codigo_error TEXT,
                intento INTEGER DEFAULT 1,
                fuente TEXT DEFAULT 'tusdatos.co'
            )
        ''')
        
        # Tabla de métricas para consultas paralelas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metricas_paralelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                total_consultas INTEGER,
                exitosas INTEGER,
                fallidas INTEGER,
                tiempo_total REAL,
                tiempo_promedio REAL,
                tiempo_minimo REAL,
                tiempo_maximo REAL,
                bloqueos_detectados INTEGER,
                tasa_exito REAL,
                fecha_ejecucion TEXT,
                worker_count INTEGER
            )
        ''')
        
        # Tabla de logs de errores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_errores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                documento TEXT,
                tipo_error TEXT,
                mensaje_error TEXT,
                stack_trace TEXT,
                resolved BOOLEAN DEFAULT 0
            )
        ''')
        
        # Índices para mejor performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documento ON consultas(documento)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON consultas(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_exitosas ON consultas(consulta_exitosa)')
        
        conn.commit()
        conn.close()
        logger.info("✅ Base de datos inicializada con 3 tablas")
    
    def save_consulta(self, data: Dict[str, Any]) -> int:
        """
        Guarda los datos de una consulta en la base de datos
        
        Args:
            data: Diccionario con los datos de la consulta
            
        Returns:
            ID del registro insertado
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Campos obligatorios
        required = ['documento', 'consulta_exitosa']
        for field in required:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        # Valores por defecto
        defaults = {
            'timestamp': datetime.now().isoformat(),
            'nombre': '',
            'fecha_expedicion': None,
            'estado_vigencia': None,
            'pdf_path': None,
            'tiempo_respuesta': 0.0,
            'codigo_error': None,
            'intento': 1
        }
        
        # Combinar datos con defaults
        full_data = {**defaults, **data}
        
        try:
            cursor.execute('''
                INSERT INTO consultas 
                (timestamp, documento, nombre, fecha_expedicion, fecha_nacimiento,
                 lugar_expedicion, estado_vigencia, direccion, pdf_path,
                 consulta_exitosa, tiempo_respuesta, codigo_error, intento, fuente)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                full_data['timestamp'],
                full_data['documento'],
                full_data.get('nombre'),
                full_data.get('fecha_expedicion'),
                full_data.get('fecha_nacimiento'),
                full_data.get('lugar_expedicion'),
                full_data.get('estado_vigencia'),
                full_data.get('direccion'),
                full_data.get('pdf_path'),
                full_data['consulta_exitosa'],
                full_data['tiempo_respuesta'],
                full_data.get('codigo_error'),
                full_data.get('intento', 1),
                full_data.get('fuente', 'tusdatos.co')
            ))
            
            conn.commit()
            consulta_id = cursor.lastrowid
            logger.info(f"✅ Consulta guardada ID: {consulta_id} - Documento: {full_data['documento']}")
            
            return consulta_id
            
        except sqlite3.Error as e:
            logger.error(f"❌ Error guardando consulta: {e}")
            raise
        finally:
            conn.close()
    
    def save_metricas_paralelas(self, metricas: Dict[str, Any]) -> int:
        """
        Guarda métricas de ejecuciones paralelas
        
        Args:
            metricas: Diccionario con métricas
            
        Returns:
            ID del registro insertado
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO metricas_paralelas 
                (session_id, total_consultas, exitosas, fallidas, tiempo_total,
                 tiempo_promedio, tiempo_minimo, tiempo_maximo, bloqueos_detectados,
                 tasa_exito, fecha_ejecucion, worker_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metricas.get('session_id', datetime.now().strftime('%Y%m%d_%H%M%S')),
                metricas.get('total_consultas', 0),
                metricas.get('exitosas', 0),
                metricas.get('fallidas', 0),
                metricas.get('tiempo_total', 0),
                metricas.get('tiempo_promedio', 0),
                metricas.get('tiempo_minimo', 0),
                metricas.get('tiempo_maximo', 0),
                metricas.get('bloqueos_detectados', 0),
                metricas.get('tasa_exito', 0),
                datetime.now().isoformat(),
                metricas.get('worker_count', 15)
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        except sqlite3.Error as e:
            logger.error(f"Error guardando métricas: {e}")
            raise
        finally:
            conn.close()
    
    def export_to_csv(self, filename: str = "consultas.csv") -> Path:
        """Exporta todas las consultas a CSV"""
        conn = sqlite3.connect(self.db_name)
        
        try:
            df = pd.read_sql_query("SELECT * FROM consultas ORDER BY timestamp DESC", conn)
            
            csv_path = self.output_dir / filename
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            logger.info(f"✅ Datos exportados a CSV: {csv_path} ({len(df)} registros)")
            return csv_path
            
        finally:
            conn.close()
    
    def export_to_json(self, filename: str = "consultas.json") -> Path:
        """Exporta consultas a JSON"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM consultas ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            data = [dict(row) for row in rows]
            
            json_path = self.output_dir / filename
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Datos exportados a JSON: {json_path} ({len(data)} registros)")
            return json_path
            
        finally:
            conn.close()
    
    def export_to_excel(self, filename: str = "consultas.xlsx") -> Path:
        """Exporta consultas a Excel"""
        conn = sqlite3.connect(self.db_name)
        
        try:
            # Consultas principales
            df_consultas = pd.read_sql_query("SELECT * FROM consultas", conn)
            
            # Métricas
            df_metricas = pd.read_sql_query("SELECT * FROM metricas_paralelas", conn)
            
            excel_path = self.output_dir / filename
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df_consultas.to_excel(writer, sheet_name='Consultas', index=False)
                df_metricas.to_excel(writer, sheet_name='Métricas', index=False)
            
            logger.info(f"✅ Datos exportados a Excel: {excel_path}")
            return excel_path
            
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas"""
        conn = sqlite3.connect(self.db_name)
        
        try:
            cursor = conn.cursor()
            
            # Estadísticas básicas
            cursor.execute('SELECT COUNT(*) FROM consultas')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM consultas WHERE consulta_exitosa = 1')
            exitosas = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(tiempo_respuesta) FROM consultas WHERE consulta_exitosa = 1')
            avg_time = cursor.fetchone()[0] or 0
            
            # Últimas consultas
            cursor.execute('''
                SELECT documento, nombre, estado_vigencia, tiempo_respuesta 
                FROM consultas 
                WHERE consulta_exitosa = 1 
                ORDER BY timestamp DESC 
                LIMIT 5
            ''')
            ultimas = cursor.fetchall()
            
            # Distribución por día
            cursor.execute('''
                SELECT DATE(timestamp) as fecha, COUNT(*) as cantidad
                FROM consultas
                GROUP BY DATE(timestamp)
                ORDER BY fecha DESC
                LIMIT 7
            ''')
            por_dia = cursor.fetchall()
            
            return {
                'total_consultas': total,
                'consultas_exitosas': exitosas,
                'consultas_fallidas': total - exitosas,
                'tasa_exito': (exitosas / total * 100) if total > 0 else 0,
                'tiempo_promedio': round(avg_time, 2),
                'ultimas_consultas': [
                    {'documento': r[0], 'nombre': r[1], 'estado': r[2], 'tiempo': r[3]}
                    for r in ultimas
                ],
                'consultas_ultima_semana': [
                    {'fecha': r[0], 'cantidad': r[1]} for r in por_dia
                ]
            }
            
        finally:
            conn.close()
    
    def get_consulta_by_documento(self, documento: str) -> Optional[Dict[str, Any]]:
        """Busca una consulta por número de documento"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM consultas 
                WHERE documento = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (documento,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        finally:
            conn.close()
    
    def log_error(self, documento: Optional[str], error_type: str, 
                  error_msg: str, stack_trace: str = None) -> int:
        """Registra un error en la base de datos"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO logs_errores 
                (timestamp, documento, tipo_error, mensaje_error, stack_trace)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                documento,
                error_type,
                error_msg,
                stack_trace
            ))
            
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()


# Funciones de utilidad
def backup_database(source_db: str = "consultas_registraduria.db"):
    """Crea un backup de la base de datos"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"backup_{timestamp}.db"
    
    import shutil
    shutil.copy2(source_db, backup_file)
    
    logger.info(f"✅ Backup creado: {backup_file}")
    return backup_file


def cleanup_old_backups(days_to_keep: int = 7):
    """Elimina backups antiguos"""
    import time
    backup_dir = Path("backups")
    
    if not backup_dir.exists():
        return
    
    current_time = time.time()
    cutoff = current_time - (days_to_keep * 86400)
    
    for backup_file in backup_dir.glob("backup_*.db"):
        if backup_file.stat().st_mtime < cutoff:
            backup_file.unlink()
            logger.info(f"🗑️  Backup eliminado: {backup_file}")


# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Probando sistema de almacenamiento...")
    
    # Inicializar
    storage = DataStorage()
    
    # Guardar ejemplo de consulta
    ejemplo_data = {
        'documento': '123456789',
        'nombre': 'JUAN CARLOS PEREZ',
        'fecha_expedicion': '2023-01-15',
        'estado_vigencia': 'VIGENTE',
        'consulta_exitosa': True,
        'tiempo_respuesta': 2.5,
        'pdf_path': 'pdfs/123456789.pdf'
    }
    
    consulta_id = storage.save_consulta(ejemplo_data)
    print(f"✅ Consulta guardada con ID: {consulta_id}")
    
    # Exportar datos
    storage.export_to_csv()
    storage.export_to_json()
    storage.export_to_excel()
    
    # Obtener estadísticas
    stats = storage.get_stats()
    print("\n📊 Estadísticas:")
    for key, value in stats.items():
        if key not in ['ultimas_consultas', 'consultas_ultima_semana']:
            print(f"  {key}: {value}")
    
    # Buscar consulta
    consulta = storage.get_consulta_by_documento('123456789')
    if consulta:
        print(f"\n🔍 Consulta encontrada: {consulta['nombre']}")
    
    # Crear backup
    backup_database()
    
    print("\n🎉 Sistema de almacenamiento probado exitosamente!")
