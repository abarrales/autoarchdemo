#!/bin/bash

# Script para solucionar error 413 (Request Entity Too Large) en Nginx
# Uso: ./fix-nginx-upload.sh

echo "🔧 Solucionando error 413 - Request Entity Too Large"

# Verificar si nginx está instalado
if ! command -v nginx &> /dev/null; then
    echo "❌ Nginx no está instalado"
    exit 1
fi

# Backup del archivo de configuración
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup creado en /etc/nginx/nginx.conf.backup.$(date +%Y%m%d_%H%M%S)"

# Verificar si la configuración ya existe
if grep -q "client_max_body_size" /etc/nginx/nginx.conf; then
    echo "⚠️  client_max_body_size ya existe en la configuración"
    echo "📝 Actualizando valor a 10M..."
    sudo sed -i 's/client_max_body_size.*$/client_max_body_size 10M;/' /etc/nginx/nginx.conf
else
    echo "📝 Agregando client_max_body_size 10M a la configuración..."
    sudo sed -i '/http {/a\    client_max_body_size 10M;' /etc/nginx/nginx.conf
fi

# Verificar sintaxis de nginx
echo "🔍 Verificando sintaxis de nginx..."
if sudo nginx -t; then
    echo "✅ Sintaxis correcta"
    echo "🔄 Recargando nginx..."
    sudo nginx -s reload
    echo "✅ Nginx recargado exitosamente"
    echo "🎉 Error 413 solucionado - Ahora puedes subir archivos hasta 10MB"
else
    echo "❌ Error en la sintaxis de nginx"
    echo "🔄 Restaurando backup..."
    sudo cp /etc/nginx/nginx.conf.backup.$(date +%Y%m%d_%H%M%S) /etc/nginx/nginx.conf
    echo "❌ Configuración restaurada"
    exit 1
fi