#!/usr/bin/env python3
"""
Script para ejecutar el bot de WhatsApp
"""

import os
import sys
from whatsapp_bot import app

def check_environment():
    """Verificar que las variables de entorno estén configuradas"""
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_WHATSAPP_NUMBER',
        'GOOGLE_EMAIL',
        'GOOGLE_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Error: Faltan las siguientes variables de entorno:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Crea un archivo .env basado en env_example.txt")
        print("💡 Ejecuta: cp env_example.txt .env")
        return False
    
    return True

def main():
    """Función principal"""
    print("🤖 Iniciando Bot de WhatsApp para Google Maps...")
    
    # Verificar configuración
    if not check_environment():
        sys.exit(1)
    
    print("✅ Configuración verificada")
    print("🌐 Iniciando servidor web en http://localhost:5000")
    print("📱 El bot estará disponible en el webhook: http://localhost:5000/webhook")
    print("\n⚠️  IMPORTANTE:")
    print("   - Configura tu webhook en Twilio para apuntar a tu servidor")
    print("   - Usa ngrok o similar para exponer tu servidor local")
    print("   - Ejemplo: ngrok http 5000")
    print("\n🔄 Presiona Ctrl+C para detener el bot")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Bot detenido")

if __name__ == '__main__':
    main() 