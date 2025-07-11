#!/bin/bash

# Script para ejecutar el bot de WhatsApp con Docker

echo "🤖 Iniciando WhatsApp Feedback Bot con Docker..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    exit 1
fi

# Verificar que docker-compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose no está instalado"
    exit 1
fi

# Verificar que el archivo .env exista
if [ ! -f .env ]; then
    echo "⚠️  Advertencia: Archivo .env no encontrado"
    echo "📝 Crea el archivo .env basado en env_example.txt"
    echo "💡 Ejecuta: cp env_example.txt .env"
    echo ""
    read -p "¿Quieres continuar sin el archivo .env? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  -d, --dev     Modo desarrollo (con hot reload)"
    echo "  -p, --prod    Modo producción"
    echo "  -n, --ngrok   Incluir ngrok para desarrollo"
    echo "  -m, --monitor Incluir monitoreo (Prometheus + Grafana)"
    echo "  -h, --help    Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 --dev      # Modo desarrollo"
    echo "  $0 --dev --ngrok  # Desarrollo con ngrok"
    echo "  $0 --prod     # Modo producción"
}

# Procesar argumentos
MODE="prod"
INCLUDE_NGROK=false
INCLUDE_MONITORING=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dev)
            MODE="dev"
            shift
            ;;
        -p|--prod)
            MODE="prod"
            shift
            ;;
        -n|--ngrok)
            INCLUDE_NGROK=true
            shift
            ;;
        -m|--monitor)
            INCLUDE_MONITORING=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "❌ Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Construir comando docker-compose
COMPOSE_FILES="-f docker-compose.yml"

if [ "$MODE" = "dev" ]; then
    COMPOSE_FILES="$COMPOSE_FILES -f docker-compose.override.yml"
    echo "🔧 Modo desarrollo activado"
fi

if [ "$INCLUDE_NGROK" = true ]; then
    COMPOSE_FILES="$COMPOSE_FILES --profile development"
    echo "🌐 Ngrok incluido"
fi

if [ "$INCLUDE_MONITORING" = true ]; then
    COMPOSE_FILES="$COMPOSE_FILES --profile monitoring"
    echo "📊 Monitoreo incluido"
fi

echo "🚀 Ejecutando: docker-compose $COMPOSE_FILES up"
echo ""

# Ejecutar docker-compose
docker-compose $COMPOSE_FILES up 