#!/usr/bin/env python3
"""
Aplicación principal del Bot de WhatsApp para Google Maps
"""

import os
import sys
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

# Agregar src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.bot import WhatsAppBot
from src.config import Config

# Crear instancia global del bot
bot = WhatsAppBot()
config = Config()

# Configurar Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para Docker"""
    return jsonify({
        'status': 'healthy',
        'service': 'whatsapp-feedback-bot',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook para recibir mensajes de Twilio"""
    try:
        # Obtener datos del mensaje
        from_number = request.form.get('From', '').replace('whatsapp:', '')
        message_body = request.form.get('Body', '')
        media_urls = []
        
        # Obtener URLs de medios si los hay
        num_media = int(request.form.get('NumMedia', 0))
        for i in range(num_media):
            media_url = request.form.get(f'MediaUrl{i}', '')
            if media_url:
                media_urls.append(media_url)
                
        # Procesar mensaje
        response_message = bot.handle_incoming_message(from_number, message_body, media_urls)
        
        # Crear respuesta TwiML
        resp = MessagingResponse()
        resp.message(response_message)
        
        return str(resp)
        
    except Exception as e:
        bot.logger.error(f"Error en webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Lo siento, hubo un error. Por favor, intenta de nuevo.")
        return str(resp)

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({
        'message': 'WhatsApp Feedback Bot para Google Maps',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'webhook': '/webhook',
            'index': '/'
        }
    })

if __name__ == '__main__':
    # Verificar configuración
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
        sys.exit(1)
    
    print("🤖 Iniciando Bot de WhatsApp para Google Maps...")
    print("✅ Configuración verificada")
    print("🌐 Iniciando servidor web en http://localhost:5000")
    print("📱 El bot estará disponible en el webhook: http://localhost:5000/webhook")
    
    app.run(
        debug=config.FLASK_DEBUG,
        host='0.0.0.0',
        port=5000
    ) 