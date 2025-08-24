#!/bin/bash

echo "🏗️ AWS Architecture Enhancer"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 requerido"
    exit 1
fi

# Crear/activar entorno virtual
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
python3 -m pip install -r requirements.txt

# Verificar credenciales AWS (opcional)
if ! aws sts get-caller-identity &> /dev/null; then
    echo "⚠️  Credenciales AWS no configuradas - usando modo fallback"
else
    echo "✅ Credenciales AWS detectadas"
fi

# Ejecutar aplicación
echo "🚀 Iniciando Streamlit..."
streamlit run app.py