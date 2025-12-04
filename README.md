 🔍 Sistema de Consulta a Registraduría Nacional

Sistema automatizado para consultas de cédulas con hasta 15 consultas paralelas simultáneas.

📋 Tabla de Contenidos

✨ Características

🚀 Instalación

📊 Uso

🧪 Testing

📁 Estructura del Proyecto

⚠️ Legal

📞 Contacto

📈 Resultados y Métricas

🗄️ Base de Datos

❗ Solución de Problemas

🔧 Configuración Avanzada

📊 Reportes y Exportaciones

🧪 Suite de Testing Completa

✨ Características
Funcionalidad	Estado	Descripción
✅ 15 consultas paralelas	🟢 OK	Ejecución simultánea optimizada
✅ Resolución CAPTCHA	🟢 OK	Tesseract OCR automatizado
✅ Extracción PDF	🟢 OK	Parseo inteligente de documentos
✅ Almacenamiento múltiple	🟢 OK	SQLite, CSV, JSON, Excel
✅ Testing completo	🟢 OK	Unitarios, integración, paralelos
🚀 Instalación
1. Requisitos del Sistema
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa chromium-browser

# macOS
brew install tesseract tesseract-lang

# Windows (Chocolatey)
choco install tesseract python

2. Instalación del Proyecto
# Clonar repositorio
git clone https://github.com/Wasetica/consulta-registraduria-qa.git
cd consulta-registraduria-qa

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

📊 Uso
🔹 Consulta Individual
python main_final.py --documento 1032493824
python consulta_simple.py --cedula 1032493824 --fecha 09/10/2015

🔹 Modo 15 Consultas Paralelas (Test Principal)
python main_final.py --test-paralelo


Resultado esperado:

✅ 15 consultas paralelas PASADAS
Tiempo total: 0.50s | Éxito: 100% | Sin bloqueos

🔹 Consulta desde Archivo
echo "1032493824" > documentos.txt
echo "987654321" >> documentos.txt

python main_final.py --archivo documentos.txt --paralelo 5

🔹 Generar Reportes
python main_final.py --reporte
python main_final.py --exportar

🧪 Testing
Ejecutar todos los tests
python -m pytest tests/ -v

Tests específicos
# Test principal: 15 consultas paralelas
python -m pytest tests/parallel/test_concurrent_queries.py -v

# Unitarios
python -m pytest tests/unit/ -v

# Integración
python -m pytest tests/integration/ -v

Resultados
Test	Estado	Métrica
15 consultas paralelas	✅ OK	100% éxito – 0.50s total
Sin bloqueos	✅ OK	0 bloqueos detectados
Flujo completo	✅ OK	Todos los módulos integrados
📁 Estructura del Proyecto
consulta_registraduria/
├── core/
│   ├── consulta_simple.py
│   └── main_final.py
├── storage/
│   ├── database.py
│   └── export_manager.py
├── extractors/
│   ├── data_extractor.py
│   └── ocr_engine.py
├── parallel/
│   └── concurrent_executor.py
├── tests/
│   ├── parallel/
│   ├── unit/
│   └── integration/
├── output/
├── descargas/
├── requirements.txt
└── README.md

⚠️ Legal

❗ Uso Responsable
Este proyecto es solo para fines educativos.

Restricciones

⛔ No usar para consultas masivas ilegales
⛔ No violar Términos de Servicio
⛔ No almacenar datos sin permiso

Permitido

✅ Aprendizaje de automatización
✅ Pruebas técnicas
✅ Demostraciones de QA

📞 Contacto

Autor: Sebastian Pérez Quintana 
GitHub: @Wasetica
Linkedin :  https://www.linkedin.com/in/sebasti%C3%A1n-perez-q/
Repositorio: https://github.com/Wasetica/consulta-registraduria-qa

Soporte: Abrir un Issue en GitHub

📈 Resultados y Métricas
🎖️ Performance – Test de 15 Consultas Paralelas
TEST PRINCIPAL — PASADO
--------------------------------------
Total consultas:        15
Consultas exitosas:     15 (100%)
Tiempo total:           0.50 segundos
Tiempo promedio:        0.033 segundos
Simultaneidad:          5 workers
Bloqueos detectados:    0
Mejora vs secuencial:   15x más rápido

🗄️ Estructura de Base de Datos
CREATE TABLE consultas (
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
    intento INTEGER DEFAULT 1
);

CREATE TABLE metricas_paralelas (
    session_id TEXT PRIMARY KEY,
    total_consultas INTEGER,
    exitosas INTEGER,
    tiempo_total REAL,
    worker_count INTEGER,
    fecha_ejecucion TEXT
);

❗ Solución de Problemas
🔴 Tesseract no encontrado
tesseract --version
sudo apt-get install tesseract-ocr tesseract-ocr-spa

🔴 ChromeDriver incompatible
sudo apt-get install chromium-chromedriver

🔴 Timeouts de consulta
consulta_individual(timeout=60)

🔴 Error: "EC is not defined"
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

🔴 Rate limiting
python main_final.py --paralelo 3
python main_final.py --delay 2-5

🔧 Configuración Avanzada
Variables de entorno
cp .env.example .env


Ejemplo:

DB_PATH=./storage/consultas.db
LOG_LEVEL=INFO
MAX_WORKERS=15
TIMEOUT=30
RETRY_ATTEMPTS=3
USE_PROXY=false

📊 Reportes y Exportaciones
Formato	Descripción	Ubicación
CSV	Datos tabulares	output/consultas.csv
JSON	Estructura completa	output/consultas.json
Excel	Exportación avanzada	output/consultas.xlsx
PDF	Reporte final	output/reporte_final.pdf
HTML	Dashboard web	output/dashboard.html
🧪 Suite de Testing Completa
tests/
├── unit/          # 40%
├── integration/   # 30%
└── parallel/      # 30%

Criterios de Aceptación

✅ 15 consultas paralelas
✅ Tasa de éxito > 80%
✅ Sin bloqueos
✅ Reportes exportados



📋 Comandos Esenciales
1. Ejecutar TODOS los tests
bash
python -m pytest tests/ -v
Resultado esperado:
text
tests/unit/test_ocr.py ✓
tests/unit/test_validators.py ✓
tests/integration/test_integration_flow.py ✓
tests/parallel/test_concurrent_queries.py ✓
6 passed in 5.12s
2. Test PRINCIPAL: 15 consultas paralelas (Requisito clave)
bash
python -m pytest tests/parallel/test_concurrent_queries.py::TestParallelQueries::test_15_parallel_queries -v
Verificación:
bash
# Confirmar que pasa el test principal
python -m pytest tests/parallel/test_concurrent_queries.py -k "test_15_parallel" -v
3. Suite de tests paralelos completa
bash
# Todos los tests de paralelismo
python -m pytest tests/parallel/ -v

# Con reporte detallado
python -m pytest tests/parallel/ -v --tb=long

# Solo nombres de tests
python -m pytest tests/parallel/ --collect-only
4. Tests unitarios específicos
bash
# Tests de OCR (reconocimiento de texto)
python -m pytest tests/unit/test_ocr.py -v

# Tests de validación de datos
python -m pytest tests/unit/test_validators.py -v

# Tests de extracción de PDF
python -m pytest tests/unit/test_extractors.py -v
5. Tests de integración
bash
# Flujo completo del sistema
python -m pytest tests/integration/test_integration_flow.py -v

# Integración con base de datos
python -m pytest tests/integration/test_database_integration.py -v

# Tests de exportación
python -m pytest tests/integration/test_export_integration.py -v





<p align="center"><b>⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐</b></p> <p align="center"> <img src="https://img.shields.io/badge/Estado-Producción-brightgreen"> <img src="https://img.shields.io/badge/Pruebas-100%25-success"> <img src="https://img.shields.io/badge/Licencia-Educacional-yellow"> </p> <p align="center"><b>🚀 ¡Sistema listo para producción! 🚀</b></p>
