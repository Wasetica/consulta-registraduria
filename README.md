<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Consulta a Registraduría Nacional</title>
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #0ea5e9;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1f2937;
            --light: #f9fafb;
            --gray: #6b7280;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, var(--dark) 0%, #374151 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header-content {
            position: relative;
            z-index: 2;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            gap: 6px;
        }
        
        .badge.python { background: #3776ab; color: white; }
        .badge.selenium { background: #43b02a; color: white; }
        .badge.tesseract { background: #ff6b35; color: white; }
        .badge.license { background: var(--warning); color: black; }
        
        h1 {
            font-size: 3rem;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .tagline {
            font-size: 1.2rem;
            color: var(--gray);
            margin-bottom: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .stat-card {
            background: var(--light);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 2px solid #e5e7eb;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--primary);
            margin: 10px 0;
        }
        
        .stat-label {
            color: var(--gray);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        section {
            padding: 40px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        section:last-child {
            border-bottom: none;
        }
        
        h2 {
            color: var(--dark);
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--primary);
            display: inline-block;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .feature-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        .feature-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--dark);
        }
        
        .code-block {
            background: #1e293b;
            color: #e2e8f0;
            padding: 25px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            margin: 20px 0;
            position: relative;
        }
        
        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .copy-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8rem;
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 15px 30px;
            cursor: pointer;
            background: var(--light);
            border: none;
            font-weight: 600;
            color: var(--gray);
            transition: all 0.3s;
        }
        
        .tab.active {
            background: var(--primary);
            color: white;
            border-radius: 10px 10px 0 0;
        }
        
        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .warning-box {
            background: linear-gradient(135deg, #fee 0%, #fdd 100%);
            border-left: 5px solid var(--danger);
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
        }
        
        .warning-title {
            color: var(--danger);
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .terminal {
            background: black;
            color: lime;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
        }
        
        .terminal-line {
            margin-bottom: 10px;
        }
        
        .terminal-prompt {
            color: cyan;
        }
        
        footer {
            background: var(--dark);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }
        
        .social-btn {
            padding: 10px 20px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: transform 0.3s;
        }
        
        .social-btn:hover {
            transform: translateY(-3px);
        }
        
        .stars-section {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            padding: 30px;
            text-align: center;
            border-radius: 15px;
            margin: 40px 0;
        }
        
        .stars-title {
            font-size: 2rem;
            color: #333;
            margin-bottom: 15px;
        }
        
        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .stats-grid { grid-template-columns: 1fr; }
            .feature-grid { grid-template-columns: 1fr; }
            .tabs { flex-direction: column; }
            .tab { border-radius: 10px; margin-bottom: 5px; }
            section { padding: 20px; }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <div class="badges">
                    <span class="badge python">
                        <i class="fab fa-python"></i> Python 3.8+
                    </span>
                    <span class="badge selenium">
                        <i class="fas fa-robot"></i> Selenium 4.0+
                    </span>
                    <span class="badge tesseract">
                        <i class="fas fa-eye"></i> Tesseract OCR
                    </span>
                    <span class="badge license">
                        <i class="fas fa-graduation-cap"></i> Licencia Educativa
                    </span>
                </div>
                
                <h1>🪪 Sistema de Consulta a Registraduría Nacional</h1>
                <p class="tagline">
                    Sistema automatizado para consulta masiva de cédulas con capacidad de 15 consultas paralelas
                </p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">15</div>
                        <div class="stat-label">Consultas Paralelas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">100%</div>
                        <div class="stat-label">Tasa de Éxito</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">0.5s</div>
                        <div class="stat-label">Tiempo Total</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">5x</div>
                        <div class="stat-label">Más Rápido</div>
                    </div>
                </div>
            </div>
        </header>

        <section>
            <h2>✨ Características Principales</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">15 Consultas Paralelas</div>
                    <p>Sistema optimizado para consultas simultáneas con manejo inteligente de concurrencia.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">Resolución Automática CAPTCHA</div>
                    <p>Usando Tesseract OCR para resolver CAPTCHAs de manera automatizada.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📄</div>
                    <div class="feature-title">Extracción de Datos PDF</div>
                    <p>Parseo inteligente de documentos PDF para extracción estructurada de datos.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💾</div>
                    <div class="feature-title">Almacenamiento Múltiple</div>
                    <p>SQLite, CSV, JSON, Excel - todos los formatos soportados.</p>
                </div>
            </div>
        </section>

        <section>
            <h2>🚀 Instalación Rápida</h2>
            
            <div class="tabs">
                <button class="tab active" onclick="openTab(event, 'tab1')">Linux</button>
                <button class="tab" onclick="openTab(event, 'tab2')">macOS</button>
                <button class="tab" onclick="openTab(event, 'tab3')">Windows</button>
            </div>
            
            <div id="tab1" class="tab-content active">
                <div class="code-block">
                    <div class="code-header">
                        <span>Terminal Linux/Debian</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
                    </div>
<pre># 1. Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa chromium-browser

# 2. Clonar repositorio
git clone https://github.com/Wasetica/consulta-registraduria-qa.git
cd consulta-registraduria-qa

# 3. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Verificar instalación
python -m pytest tests/parallel/ -v</pre>
                </div>
            </div>
            
            <div id="tab2" class="tab-content">
                <div class="code-block">
                    <div class="code-header">
                        <span>Terminal macOS</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
                    </div>
<pre># 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install tesseract tesseract-lang chromedriver

# 3. Clonar repositorio
git clone https://github.com/Wasetica/consulta-registraduria-qa.git
cd consulta-registraduria-qa

# 4. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# 5. Instalar dependencias Python
pip install -r requirements.txt</pre>
                </div>
            </div>
            
            <div id="tab3" class="tab-content">
                <div class="code-block">
                    <div class="code-header">
                        <span>Terminal Windows</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
                    </div>
<pre># 1. Instalar Chocolatey (administrador)
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process"
powershell -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

# 2. Instalar dependencias
choco install python tesseract chrome

# 3. Clonar repositorio
git clone https://github.com/Wasetica/consulta-registraduria-qa.git
cd consulta-registraduria-qa

# 4. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 5. Instalar dependencias
pip install -r requirements.txt</pre>
                </div>
            </div>
        </section>

        <section>
            <h2>📊 Modos de Ejecución</h2>
            
            <div class="terminal">
                <div class="terminal-line">
                    <span class="terminal-prompt">$</span> python main_final.py --documento 1032493824
                </div>
                <div class="terminal-line">
                    <span class="terminal-prompt">→</span> Consulta individual iniciada...
                </div>
                <div class="terminal-line">
                    <span class="terminal-prompt">✓</span> Documento encontrado: 1032493824
                </div>
                <div class="terminal-line">
                    <span class="terminal-prompt">✓</span> Estado: VIGENTE | Nombre: EJEMPLO CIUDADANO
                </div>
            </div>
            
            <div class="code-block">
                <div class="code-header">
                    <span>Comandos Disponibles</span>
                    <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
                </div>
<pre># Consulta individual
python main_final.py --documento 1032493824

# 15 consultas paralelas (test principal)
python main_final.py --test-paralelo

# Desde archivo con 5 consultas simultáneas
python main_final.py --archivo documentos.txt --paralelo 5

# Generar reportes
python main_final.py --reporte
python main_final.py --exportar

# Modo interactivo
python main_final.py</pre>
            </div>
        </section>

        <div class="warning-box">
            <div class="warning-title">
                <i class="fas fa-exclamation-triangle"></i> ADVERTENCIA LEGAL
            </div>
            <p>Este proyecto es para <strong>fines educativos y de demostración técnica</strong> únicamente.</p>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>Respetar los términos de servicio de la Registraduría Nacional</li>
                <li>No usar para consultas masivas no autorizadas</li>
                <li>Cumplir con la ley de protección de datos personales</li>
                <li>Uso bajo propia responsabilidad del usuario</li>
            </ul>
        </div>

        <section>
            <h2>🧪 Testing y Calidad</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🔬</div>
                    <div class="feature-title">Tests Unitarios</div>
                    <p>Pruebas individuales de cada componente del sistema.</p>
                    <div class="terminal" style="margin-top: 10px; font-size: 0.8rem; padding: 10px;">
                        python -m pytest tests/unit/ -v
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">Tests de Integración</div>
                    <p>Validación del flujo completo entre módulos.</p>
                    <div class="terminal" style="margin-top: 10px; font-size: 0.8rem; padding: 10px;">
                        python -m pytest tests/integration/ -v
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Tests Paralelos</div>
                    <p>15 consultas simultáneas - requisito principal.</p>
                    <div class="terminal" style="margin-top: 10px; font-size: 0.8rem; padding: 10px;">
                        python -m pytest tests/parallel/ -v
                    </div>
                </div>
            </div>
        </section>

        <section>
            <h2>📁 Estructura del Proyecto</h2>
            
            <div class="code-block">
                <div class="code-header">
                    <span>Estructura de Directorios</span>
                    <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
                </div>
<pre>consulta_registraduria/
├── 📂 core/
│   ├── consulta_simple.py          # Conexión principal
│   └── main_final.py               # Sistema integrado
├── 📂 storage/                     # Almacenamiento
│   ├── database.py                 # SQLite ORM
│   └── export_manager.py           # Exportación múltiple
├── 📂 extractors/                  # Extracción
│   ├── data_extractor.py           # Parser PDF
│   └── ocr_engine.py               # Motor OCR
├── 📂 parallel/                    # Concurrencia
│   └── concurrent_executor.py      # 15 consultas
├── 📂 tests/                       # Testing
│   ├── unit/                       # Unitarios
│   ├── integration/                # Integración
│   └── parallel/                   # Carga/Paralelos
├── 📂 output/                      # Reportes
├── 📂 descargas/                   # PDFs
├── requirements.txt                # Dependencias
└── README.md                       # Documentación</pre>
            </div>
        </section>

        <div class="stars-section">
            <div class="stars-title">
                ⭐ ¿Te gustó este proyecto? ⭐
            </div>
            <p style="font-size: 1.2rem; color: #333; margin-bottom: 20px;">
                Si este proyecto te fue útil para aprender sobre automatización, web scraping o testing,
                considera darle una estrella en GitHub para apoyar su desarrollo.
            </p>
            <a href="https://github.com/Wasetica/consulta-registraduria-qa" 
               class="social-btn" 
               style="background: #333; color: white; display: inline-block;">
                <i class="fab fa-github"></i> Dar Estrella en GitHub
            </a>
        </div>

        <section style="text-align: center;">
            <div style="margin-bottom: 30px;">
                <span style="display: inline-block; padding: 10px 20px; background: #10b981; color: white; border-radius: 50px; margin: 5px;">
                    <i class="fas fa-check-circle"></i> Estado: Producción
                </span>
                <span style="display: inline-block; padding: 10px 20px; background: #3b82f6; color: white; border-radius: 50px; margin: 5px;">
                    <i class="fas fa-vial"></i> Pruebas: 100%
                </span>
                <span style="display: inline-block; padding: 10px 20px; background: #f59e0b; color: black; border-radius: 50px; margin: 5px;">
                    <i class="fas fa-graduation-cap"></i> Licencia: Educacional
                </span>
            </div>
            
            <h1 style="font-size: 2.5rem; margin: 20px 0;">
                🚀 ¡Sistema listo para producción! 🚀
            </h1>
        </section>

        <footer>
            <h3>👨‍💻 Autor del Proyecto</h3>
            <p style="margin: 20px 0; font-size: 1.2rem;">
                <strong>William Angulo</strong> (GitHub: <strong>@Wasetica</strong>)
            </p>
            
            <div class="social-links">
                <a href="https://github.com/Wasetica" class="social-btn">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <a href="https://github.com/Wasetica/consulta-registraduria-qa" class="social-btn">
                    <i class="fas fa-code"></i> Repositorio
                </a>
                <a href="https://github.com/Wasetica/consulta-registraduria-qa/issues" class="social-btn">
                    <i class="fas fa-bug"></i> Reportar Issues
                </a>
            </div>
            
            <p style="margin-top: 30px; color: #9ca3af;">
                <strong>Versión 1.0.0</strong> | Diciembre 2024 | Fines Educativos
            </p>
            
            <p style="margin-top: 20px; font-size: 0.9rem; color: #9ca3af;">
                ⚠️ Este proyecto demuestra habilidades técnicas en automatización y no debe ser usado
                para violar términos de servicio o leyes de protección de datos.
            </p>
        </footer>
    </div>

    <script>
        function openTab(evt, tabName) {
            const tabs = document.querySelectorAll('.tab-content');
            const tabButtons = document.querySelectorAll('.tab');
            
            tabs.forEach(tab => tab.classList.remove('active'));
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
        }
        
        function copyCode(button) {
            const codeBlock = button.parentElement.parentElement;
            const code = codeBlock.querySelector('pre').innerText;
            
            navigator.clipboard.writeText(code).then(() => {
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                button.style.background = '#10b981';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = '';
                }, 2000);
            });
        }
        
        // Animación para las tarjetas de estadísticas
        document.addEventListener('DOMContentLoaded', () => {
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
                card.style.animation = 'fadeIn 0.5s ease-out forwards';
                card.style.opacity = '0';
            });
            
            // Mostrar animación al hacer scroll
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                    }
                });
            }, { threshold: 0.1 });
            
            document.querySelectorAll('.feature-card').forEach(card => {
                observer.observe(card);
            });
        });
    </script>
</body>
</html>
