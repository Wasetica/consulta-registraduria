import re

def fix_indentation(text):
    """Corrige indentación de manera inteligente"""
    lines = text.split('\n')
    fixed = []
    
    for line in lines:
        stripped = line.strip()
        
        # Reglas de indentación
        if stripped.startswith('def ') or stripped.startswith('class '):
            indent = 0
        elif stripped.startswith('try:') or stripped.startswith('except') or stripped.startswith('finally:'):
            indent = 8
        elif stripped.startswith('from ') or stripped.startswith('import '):
            indent = 12 if 'try:' in '\n'.join(fixed[-10:]) else 8
        elif stripped.startswith('logger.') or stripped.startswith('chrome_options') or stripped.startswith('self.'):
            indent = 12 if 'try:' in '\n'.join(fixed[-10:]) else 8
        elif not stripped:
            indent = len(line) - len(line.lstrip())
        else:
            # Mantener la indentación actual si no es un problema claro
            indent = len(line) - len(line.lstrip())
        
        fixed.append(' ' * indent + stripped if stripped else '')
    
    return '\n'.join(fixed)

# Leer archivo
with open('consulta_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Aplicar corrección
fixed_content = fix_indentation(content)

# Guardar
with open('consulta_simple.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Archivo completamente reindentado")
