import sys

with open('consulta_simple.py', 'r') as f:
    lines = f.readlines()

# Corregir indentaciones en el método iniciar_navegador()
in_method = False
for i, line in enumerate(lines):
    if 'def iniciar_navegador(self):' in line:
        in_method = True
        continue
    
    if in_method:
        if line.strip() and not line.startswith(' ' * 8):
            if 'from ' in line or 'import ' in line:
                # Estas líneas deberían tener 12 espacios (3 niveles)
                lines[i] = ' ' * 12 + line.lstrip()
            elif 'logger.info(' in line or 'chrome_options' in line or 'self.browser' in line:
                # Estas líneas deberían tener 12 espacios
                lines[i] = ' ' * 12 + line.lstrip()
            elif line.strip() == 'try:' or line.strip().startswith('except') or line.strip() == 'finally:':
                # Estas líneas deberían tener 8 espacios
                lines[i] = ' ' * 8 + line.lstrip()
    
    # Salir del método cuando encontramos otro método
    if in_method and line.strip() and line.startswith(' ' * 4) and 'def ' in line:
        in_method = False

with open('consulta_simple.py', 'w') as f:
    f.writelines(lines)

print("✅ Todas las indentaciones corregidas")
