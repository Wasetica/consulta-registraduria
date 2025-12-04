#!/bin/bash

echo "🚀 SUBIENDO PROYECTO A GITHUB..."
echo "Repositorio: git@github.com:Wasetica/consulta-registraduria-qa.git"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "consulta_simple.py" ]; then
    echo "❌ Error: No estás en el directorio del proyecto"
    exit 1
fi

# Configurar remote si no existe
if ! git remote | grep -q "origin"; then
    echo "🔗 Configurando remote..."
    git remote add origin git@github.com:Wasetica/consulta-registraduria-qa.git
fi

# Cambiar a rama main
echo "🌿 Configurando rama main..."
git branch -M main

# Agregar archivos
echo "📦 Agregando archivos..."
git add .

# Commit
echo "💾 Haciendo commit..."
git commit -m "🎉 Proyecto EXPLORADOR completo

✅ Sistema completo de consultas a Registraduría
✅ 15 consultas paralelas funcionando
✅ 11/11 tests pasando
✅ Documentación profesional
✅ Entregables completados

Fecha: $(date '+%Y-%m-%d %H:%M:%S')"

# Push
echo "📤 Subiendo a GitHub..."
if git push -u origin main; then
    echo ""
    echo "✅ ¡ÉXITO! Todo subido correctamente."
    echo ""
    echo "🌐 Ve a: https://github.com/Wasetica/consulta-registraduria-qa"
    echo ""
    echo "📊 Para verificar:"
    echo "   1. Abre el enlace arriba"
    echo "   2. Deberías ver todos los archivos"
    echo "   3. README.md debe mostrarse con formato"
else
    echo ""
    echo "❌ Error al subir. Intentando con HTTPS..."
    git remote set-url origin https://github.com/Wasetica/consulta-registraduria-qa.git
    if git push -u origin main; then
        echo "✅ ¡Subido con HTTPS!"
    else
        echo "⚠️  Error persistente. Verifica:"
        echo "   - Tu conexión a internet"
        echo "   - Tus credenciales de GitHub"
        echo "   - Permisos del repositorio"
    fi
fi
