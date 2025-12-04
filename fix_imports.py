#!/usr/bin/env python3
"""
Corrección rápida de imports en consulta_simple.py
"""
import re

# Leer el archivo
with open('consulta_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar donde se importa selenium y agregar EC
if 'from selenium.webdriver.common.by import By' in content:
    # Reemplazar la línea de import
    new_import = '''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC'''
    
    content = content.replace(
        'from selenium.webdriver.common.by import By',
        new_import
    )
    
    print("✅ Import de EC agregado")

# Guardar
with open('consulta_simple.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("🎯 Archivo corregido")
