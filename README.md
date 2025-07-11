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

### Opción 1: Con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Fer-Diaz/feedback.git
   cd feedback
   ```

2. **Configurar variables de entorno**
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

   # Docker Development (Optional)
   NGROK_AUTHTOKEN=your_ngrok_authtoken_here
   ```

3. **Ejecutar con Docker**
   ```bash
   # Modo producción
   docker-compose up

   # Modo desarrollo (con hot reload)
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up

   # Con ngrok para desarrollo
   ./scripts/docker-run.sh --dev --ngrok
   ```

### Opción 2: Instalación Local

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
   
   Edita el archivo `.env` con tus credenciales (ver ejemplo arriba).

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

### Con Docker

1. **Ejecutar el bot**
   ```bash
   # Modo producción
   docker-compose up

   # Modo desarrollo
   ./scripts/docker-run.sh --dev

   # Con ngrok para desarrollo
   ./scripts/docker-run.sh --dev --ngrok
   ```

2. **Detener el bot**
   ```bash
   ./scripts/docker-stop.sh
   ```

### Sin Docker

1. **Ejecutar el bot**
   ```bash
   python app.py
   ```

### Interactuar por WhatsApp

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
├── src/                      # Código fuente principal
│   ├── __init__.py          # Paquete principal
│   ├── bot/                 # Módulo del bot de WhatsApp
│   │   ├── __init__.py
│   │   └── whatsapp_bot.py  # Bot principal
│   ├── automation/          # Módulo de automatización
│   │   ├── __init__.py
│   │   └── google_maps.py   # Automatización de Google Maps
│   ├── config/              # Módulo de configuración
│   │   ├── __init__.py
│   │   └── settings.py      # Configuración y variables
│   └── utils/               # Módulo de utilidades
│       ├── __init__.py
│       ├── logger.py        # Configuración de logging
│       └── validators.py    # Validadores de datos
├── tests/                   # Tests del proyecto
│   ├── __init__.py
│   └── test_validators.py   # Tests de validadores
├── app.py                   # Aplicación principal Flask
├── requirements.txt         # Dependencias de Python
├── env_example.txt         # Ejemplo de variables de entorno
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Orquestación de servicios
├── docker-compose.override.yml # Configuración de desarrollo
├── .dockerignore          # Archivos a ignorar en Docker
├── scripts/               # Scripts de utilidad
│   ├── docker-build.sh   # Construir imagen Docker
│   ├── docker-run.sh     # Ejecutar con Docker
│   └── docker-stop.sh    # Detener contenedores
├── logs/                 # Directorio de logs
├── photos/               # Directorio para fotos
└── README.md             # Este archivo
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

### Error de Docker
```bash
# Verificar que Docker esté instalado
docker --version

# Verificar que docker-compose esté instalado
docker-compose --version

# Limpiar contenedores e imágenes
docker-compose down
docker system prune -f
```

### Error de Chrome Driver (Docker)
```bash
# El Dockerfile incluye Chrome automáticamente
# Si hay problemas, reconstruir la imagen:
docker-compose build --no-cache
```

### Error de Twilio
- Verifica que las credenciales sean correctas
- Asegúrate de que el webhook esté configurado
- Revisa que el número esté en el sandbox

### Error de Google Maps
- Verifica que las credenciales de Google sean correctas
- Asegúrate de que la cuenta no tenga 2FA habilitado
- Revisa que no haya captchas

### Error de Ngrok
- Verifica que el token de ngrok esté configurado en .env
- Revisa que el puerto 4040 esté disponible

## 📝 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 🤝 Contribuir

Pull requests son bienvenidos. Para cambios importantes, abre un issue primero para discutir qué te gustaría cambiar. 