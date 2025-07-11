from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import tempfile
import logging
from datetime import datetime
from ..config import Config
from ..automation import GoogleMapsAutomation

class WhatsAppBot:
    """Bot principal de WhatsApp para manejo de feedback"""
    
    def __init__(self):
        self.config = Config()
        self.client = Client(self.config.TWILIO_ACCOUNT_SID, self.config.TWILIO_AUTH_TOKEN)
        self.sessions = {}  # Almacenar estado de conversación por usuario
        self.setup_logging()
        
    def setup_logging(self):
        """Configurar logging del bot"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_user_session(self, user_number):
        """Obtener o crear sesión de usuario"""
        if user_number not in self.sessions:
            self.sessions[user_number] = {
                'state': None,
                'place_name': None,
                'rating': None,
                'text': None,
                'photos': [],
                'created_at': datetime.now()
            }
        return self.sessions[user_number]
        
    def send_message(self, to_number, message):
        """Enviar mensaje de WhatsApp"""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.config.TWILIO_WHATSAPP_NUMBER}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            self.logger.info(f"Mensaje enviado a {to_number}: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Error enviando mensaje: {str(e)}")
            return False
            
    def handle_incoming_message(self, from_number, message_body, media_urls=None):
        """Manejar mensaje entrante"""
        session = self.get_user_session(from_number)
        
        # Verificar si el usuario está autorizado
        if self.config.ALLOWED_NUMBERS and from_number not in self.config.ALLOWED_NUMBERS:
            return "Lo siento, no tienes autorización para usar este bot."
            
        # Procesar según el estado actual
        if session['state'] is None:
            return self.handle_welcome(from_number, message_body)
        elif session['state'] == self.config.WAITING_FOR_PLACE:
            return self.handle_place_input(from_number, message_body)
        elif session['state'] == self.config.WAITING_FOR_RATING:
            return self.handle_rating_input(from_number, message_body)
        elif session['state'] == self.config.WAITING_FOR_TEXT:
            return self.handle_text_input(from_number, message_body)
        elif session['state'] == self.config.WAITING_FOR_PHOTOS:
            return self.handle_photos_input(from_number, message_body, media_urls)
        elif session['state'] == self.config.CONFIRMING_SUBMISSION:
            return self.handle_confirmation(from_number, message_body)
            
    def handle_welcome(self, from_number, message_body):
        """Manejar mensaje de bienvenida"""
        session = self.get_user_session(from_number)
        session['state'] = self.config.WAITING_FOR_PLACE
        
        welcome_message = (
            "¡Hola! Soy tu bot de feedback para Google Maps. 🗺️\n\n"
            "Para empezar, envíame el nombre del lugar donde quieres dejar tu reseña.\n"
            "Puedes escribir el nombre del local, restaurante, o cualquier lugar."
        )
        
        self.send_message(from_number, welcome_message)
        return welcome_message
        
    def handle_place_input(self, from_number, message_body):
        """Manejar entrada del nombre del lugar"""
        session = self.get_user_session(from_number)
        session['place_name'] = message_body
        session['state'] = self.config.WAITING_FOR_RATING
        
        rating_message = (
            f"Perfecto! Buscaré: *{message_body}*\n\n"
            "Ahora califica el lugar del 1 al 5 estrellas:\n"
            "⭐ = 1 estrella\n"
            "⭐⭐ = 2 estrellas\n"
            "⭐⭐⭐ = 3 estrellas\n"
            "⭐⭐⭐⭐ = 4 estrellas\n"
            "⭐⭐⭐⭐⭐ = 5 estrellas\n\n"
            "Escribe solo el número (1, 2, 3, 4 o 5):"
        )
        
        self.send_message(from_number, rating_message)
        return rating_message
        
    def handle_rating_input(self, from_number, message_body):
        """Manejar entrada de calificación"""
        session = self.get_user_session(from_number)
        
        try:
            rating = int(message_body)
            if rating < 1 or rating > 5:
                raise ValueError("Rating fuera de rango")
        except ValueError:
            error_message = "Por favor, escribe solo un número del 1 al 5."
            self.send_message(from_number, error_message)
            return error_message
            
        session['rating'] = rating
        session['state'] = self.config.WAITING_FOR_TEXT
        
        text_message = (
            f"¡Excelente! Calificación: {'⭐' * rating}\n\n"
            "Ahora escribe tu reseña. Cuéntanos tu experiencia:\n"
            "- ¿Qué te gustó?\n"
            "- ¿Qué mejorarías?\n"
            "- ¿Recomendarías el lugar?\n\n"
            "Escribe tu comentario:"
        )
        
        self.send_message(from_number, text_message)
        return text_message
        
    def handle_text_input(self, from_number, message_body):
        """Manejar entrada de texto de la reseña"""
        session = self.get_user_session(from_number)
        session['text'] = message_body
        session['state'] = self.config.WAITING_FOR_PHOTOS
        
        photos_message = (
            "¡Perfecto! Tu reseña está lista.\n\n"
            "¿Quieres agregar fotos? Envía las imágenes que quieras incluir en tu reseña.\n"
            "Si no quieres agregar fotos, escribe 'sin fotos' o 'no'."
        )
        
        self.send_message(from_number, photos_message)
        return photos_message
        
    def handle_photos_input(self, from_number, message_body, media_urls):
        """Manejar entrada de fotos"""
        session = self.get_user_session(from_number)
        
        if message_body.lower() in ['sin fotos', 'no', 'nada']:
            session['state'] = self.config.CONFIRMING_SUBMISSION
            return self.show_confirmation(from_number)
        elif media_urls:
            # Descargar y guardar fotos temporalmente
            for url in media_urls:
                try:
                    # Aquí implementarías la descarga de la imagen
                    # Por ahora, solo guardamos la URL
                    session['photos'].append(url)
                except Exception as e:
                    self.logger.error(f"Error descargando foto: {str(e)}")
                    
            session['state'] = self.config.CONFIRMING_SUBMISSION
            return self.show_confirmation(from_number)
        else:
            error_message = "Por favor, envía las fotos o escribe 'sin fotos' si no quieres agregar imágenes."
            self.send_message(from_number, error_message)
            return error_message
            
    def show_confirmation(self, from_number):
        """Mostrar confirmación antes de enviar"""
        session = self.get_user_session(from_number)
        
        confirmation_message = (
            "📋 *Resumen de tu reseña:*\n\n"
            f"📍 *Lugar:* {session['place_name']}\n"
            f"⭐ *Calificación:* {'⭐' * session['rating']}\n"
            f"📝 *Comentario:* {session['text']}\n"
            f"📸 *Fotos:* {len(session['photos'])} imagen(es)\n\n"
            "¿Estás seguro de que quieres enviar esta reseña a Google Maps?\n"
            "Escribe 'sí' para confirmar o 'no' para cancelar."
        )
        
        self.send_message(from_number, confirmation_message)
        return confirmation_message
        
    def handle_confirmation(self, from_number, message_body):
        """Manejar confirmación final"""
        session = self.get_user_session(from_number)
        
        if message_body.lower() in ['sí', 'si', 'yes', 'ok', 'confirmar']:
            return self.submit_to_google_maps(from_number)
        elif message_body.lower() in ['no', 'cancelar', 'cancel']:
            # Limpiar sesión
            del self.sessions[from_number]
            
            cancel_message = "Reseña cancelada. Puedes empezar de nuevo enviando cualquier mensaje."
            self.send_message(from_number, cancel_message)
            return cancel_message
        else:
            error_message = "Por favor, escribe 'sí' para confirmar o 'no' para cancelar."
            self.send_message(from_number, error_message)
            return error_message
            
    def submit_to_google_maps(self, from_number):
        """Enviar reseña a Google Maps"""
        session = self.get_user_session(from_number)
        
        try:
            # Crear instancia de automatización
            automation = GoogleMapsAutomation(
                self.config.GOOGLE_EMAIL,
                self.config.GOOGLE_PASSWORD
            )
            
            # Procesar feedback
            success, message = automation.process_feedback(
                session['place_name'],
                session['rating'],
                session['text'],
                session['photos'] if session['photos'] else None
            )
            
            if success:
                success_message = (
                    "✅ *¡Reseña enviada exitosamente!*\n\n"
                    f"Tu reseña para *{session['place_name']}* ya está publicada en Google Maps.\n"
                    "¡Gracias por compartir tu experiencia!"
                )
            else:
                error_message = (
                    "❌ *Error al enviar la reseña*\n\n"
                    f"Error: {message}\n"
                    "Por favor, intenta de nuevo más tarde."
                )
                
            # Limpiar sesión
            del self.sessions[from_number]
            
            self.send_message(from_number, success_message if success else error_message)
            return success_message if success else error_message
            
        except Exception as e:
            self.logger.error(f"Error en submit_to_google_maps: {str(e)}")
            error_message = "❌ Error interno del bot. Por favor, intenta de nuevo."
            self.send_message(from_number, error_message)
            return error_message 