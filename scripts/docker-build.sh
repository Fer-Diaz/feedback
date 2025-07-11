#!/bin/bash

# Script para construir la imagen Docker del bot de WhatsApp

echo "🐳 Construyendo imagen Docker para WhatsApp Feedback Bot..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    exit 1
fi

# Construir la imagen
docker build -t feedback-whatsapp-bot .

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
    echo "📋 Para ejecutar el bot:"
    echo "   docker-compose up"
    echo ""
    echo "📋 Para ejecutar en modo desarrollo:"
    echo "   docker-compose -f docker-compose.yml -f docker-compose.override.yml up"
else
    echo "❌ Error construyendo la imagen"
    exit 1
fi 