import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración del bot de WhatsApp para Google Maps"""
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    # Google Maps Configuration
    GOOGLE_EMAIL = os.getenv('GOOGLE_EMAIL')
    GOOGLE_PASSWORD = os.getenv('GOOGLE_PASSWORD')
    
    # Bot Configuration
    BOT_NAME = "FeedbackBot"
    ALLOWED_NUMBERS = os.getenv('ALLOWED_NUMBERS', '').split(',')  # Números autorizados
    
    # Session States
    WAITING_FOR_PLACE = "waiting_for_place"
    WAITING_FOR_RATING = "waiting_for_rating"
    WAITING_FOR_TEXT = "waiting_for_text"
    WAITING_FOR_PHOTOS = "waiting_for_photos"
    CONFIRMING_SUBMISSION = "confirming_submission"
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')
    
    # Docker Configuration
    NGROK_AUTHTOKEN = os.getenv('NGROK_AUTHTOKEN') 