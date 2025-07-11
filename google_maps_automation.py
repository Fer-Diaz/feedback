import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class GoogleMapsAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Configurar el driver de Chrome con opciones optimizadas"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Mantener el navegador abierto para debugging
        # chrome_options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login_to_google(self):
        """Iniciar sesión en Google"""
        try:
            self.logger.info("Iniciando sesión en Google...")
            self.driver.get("https://accounts.google.com/signin")
            
            # Esperar y llenar email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            email_input.send_keys(self.email)
            
            # Click en siguiente
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            # Esperar y llenar contraseña
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(self.password)
            
            # Click en siguiente
            password_next = self.driver.find_element(By.ID, "passwordNext")
            password_next.click()
            
            # Esperar a que se complete el login
            time.sleep(5)
            self.logger.info("Login completado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante el login: {str(e)}")
            return False
            
    def search_place(self, place_name):
        """Buscar un lugar en Google Maps"""
        try:
            self.logger.info(f"Buscando lugar: {place_name}")
            self.driver.get("https://www.google.com/maps")
            
            # Esperar y llenar la búsqueda
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.clear()
            search_box.send_keys(place_name)
            
            # Presionar Enter
            search_box.send_keys("\n")
            
            # Esperar a que carguen los resultados
            time.sleep(3)
            
            # Hacer click en el primer resultado
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-result-index='0']"))
            )
            first_result.click()
            
            time.sleep(3)
            self.logger.info("Lugar encontrado y seleccionado")
            return True
            
        except Exception as e:
            self.logger.error(f"Error buscando lugar: {str(e)}")
            return False
            
    def submit_review(self, rating, text, photos=None):
        """Enviar una reseña al lugar actual"""
        try:
            self.logger.info("Iniciando proceso de envío de reseña...")
            
            # Buscar y hacer click en el botón de reseñas
            reviews_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='reseña'], button[aria-label*='review']"))
            )
            reviews_button.click()
            
            time.sleep(2)
            
            # Buscar y hacer click en "Escribir reseña"
            write_review_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Escribir reseña'], button[aria-label*='Write a review']"))
            )
            write_review_button.click()
            
            time.sleep(2)
            
            # Seleccionar rating (1-5 estrellas)
            rating_selector = f"button[aria-label*='{rating} estrella'], button[aria-label*='{rating} star']"
            rating_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, rating_selector))
            )
            rating_button.click()
            
            # Escribir texto de la reseña
            review_text_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label*='reseña'], textarea[aria-label*='review']"))
            )
            review_text_area.clear()
            review_text_area.send_keys(text)
            
            # Subir fotos si las hay
            if photos:
                for photo_path in photos:
                    if os.path.exists(photo_path):
                        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                        file_input.send_keys(photo_path)
                        time.sleep(2)
            
            # Enviar la reseña
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Enviar'], button[aria-label*='Submit']"))
            )
            submit_button.click()
            
            time.sleep(3)
            self.logger.info("Reseña enviada exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error enviando reseña: {str(e)}")
            return False
            
    def close(self):
        """Cerrar el navegador"""
        if self.driver:
            self.driver.quit()
            
    def process_feedback(self, place_name, rating, text, photos=None):
        """Proceso completo de feedback"""
        try:
            self.setup_driver()
            
            if not self.login_to_google():
                return False, "Error en el login de Google"
                
            if not self.search_place(place_name):
                return False, "Error buscando el lugar"
                
            if not self.submit_review(rating, text, photos):
                return False, "Error enviando la reseña"
                
            return True, "Reseña enviada exitosamente"
            
        except Exception as e:
            return False, f"Error general: {str(e)}"
        finally:
            self.close() 