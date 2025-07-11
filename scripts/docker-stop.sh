#!/bin/bash

# Script para detener el bot de WhatsApp con Docker

echo "🛑 Deteniendo WhatsApp Feedback Bot..."

# Verificar que docker-compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose no está instalado"
    exit 1
fi

# Detener todos los servicios
docker-compose down

echo "✅ Servicios detenidos"

# Mostrar estado de contenedores
echo ""
echo "📋 Estado de contenedores:"
docker-compose ps 