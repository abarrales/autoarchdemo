#!/bin/bash

echo "🚀 Instalador Amazon Q Developer CLI para Ubuntu ARM64"

# Actualizar sistema e instalar dependencias
echo "📦 Actualizando sistema e instalando dependencias..."
sudo apt update -y
sudo apt install curl unzip -y

# Descargar Amazon Q CLI
echo "⬇️ Descargando Amazon Q CLI..."
curl --proto '=https' --tlsv1.2 -sSf "https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip" -o "q.zip"

# Extraer e instalar
echo "📂 Extrayendo archivos..."
unzip q.zip

echo "🔧 Instalando Amazon Q CLI..."
bash ./q/install.sh

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
rm -rf q.zip q/

echo "✅ Instalación completada!"
echo "💡 Ejecuta 'q --version' para verificar la instalación"
echo "💡 Ejecuta 'q configure' para configurar tus credenciales"