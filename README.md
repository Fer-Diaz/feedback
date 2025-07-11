# Feedback Bot para Google Maps

Un bot de WhatsApp que permite enviar reseñas y feedback directamente a Google Maps de forma automatizada.

## 🚀 Características

- **Bot de WhatsApp**: Interfaz conversacional intuitiva
- **Automatización de Google Maps**: Sube reseñas automáticamente usando Selenium
- **Sistema de calificación**: Puntuación del 1 al 5 estrellas
- **Soporte para fotos**: Incluye imágenes en las reseñas
- **Confirmación antes de enviar**: Resumen y confirmación final
- **Sesiones de usuario**: Manejo de conversaciones múltiples

## 📋 Requisitos

- Python 3.8+
- Cuenta de Twilio (para WhatsApp API)
- Cuenta de Google (para automatización de Maps)
- Chrome/Chromium (para Selenium)

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Fer-Diaz/feedback.git
   cd feedback
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp env_example.txt .env
   ```
   
   Edita el archivo `.env` con tus credenciales:
   ```env
   # Twilio WhatsApp Configuration
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_WHATSAPP_NUMBER=+1234567890

   # Google Maps Configuration
   GOOGLE_EMAIL=your_google_email@gmail.com
   GOOGLE_PASSWORD=your_google_password_here

   # Bot Configuration
   ALLOWED_NUMBERS=+1234567890,+0987654321
   ```

## 🔧 Configuración de Twilio

1. **Crear cuenta en Twilio**
   - Ve a [Twilio](https://www.twilio.com/try-twilio)
   - Regístrate y verifica tu cuenta

2. **Configurar WhatsApp Sandbox**
   - En el dashboard de Twilio, ve a Messaging > Try it out
   - Activa el sandbox de WhatsApp
   - Sigue las instrucciones para conectar tu número

3. **Configurar Webhook**
   - Usa ngrok para exponer tu servidor local: `ngrok http 5000`
   - Configura el webhook en Twilio: `https://tu-tunnel.ngrok.io/webhook`

## 🚀 Uso

1. **Ejecutar el bot**
   ```bash
   python run_bot.py
   ```

2. **Interactuar por WhatsApp**
   - Envía un mensaje al número de Twilio
   - Sigue las instrucciones del bot:
     1. Escribe el nombre del lugar
     2. Califica del 1 al 5
     3. Escribe tu reseña
     4. Agrega fotos (opcional)
     5. Confirma el envío

## 📁 Estructura del Proyecto

```
feedback/
├── whatsapp_bot.py          # Bot principal de WhatsApp
├── google_maps_automation.py # Automatización de Google Maps
├── config.py                # Configuración y variables
├── run_bot.py              # Script de ejecución
├── requirements.txt        # Dependencias de Python
├── env_example.txt        # Ejemplo de variables de entorno
└── README.md              # Este archivo
```

## ⚠️ Consideraciones Importantes

- **Autenticación de Google**: El bot usa tus credenciales de Google para subir reseñas
- **Automatización**: Usa Selenium para automatizar Google Maps (puede ser detectado)
- **Límites de Google**: Respeta los términos de servicio de Google
- **Seguridad**: No compartas tus credenciales en el código

## 🔒 Seguridad

- Usa variables de entorno para credenciales
- Limita el acceso con `ALLOWED_NUMBERS`
- Considera usar autenticación de dos factores en Google
- Revisa regularmente los logs de actividad

## 🐛 Solución de Problemas

### Error de Chrome Driver
```bash
# Instalar Chrome si no está instalado
# El webdriver-manager se encarga automáticamente
```

### Error de Twilio
- Verifica que las credenciales sean correctas
- Asegúrate de que el webhook esté configurado
- Revisa que el número esté en el sandbox

### Error de Google Maps
- Verifica que las credenciales de Google sean correctas
- Asegúrate de que la cuenta no tenga 2FA habilitado
- Revisa que no haya captchas

## 📝 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 🤝 Contribuir

Pull requests son bienvenidos. Para cambios importantes, abre un issue primero para discutir qué te gustaría cambiar. 