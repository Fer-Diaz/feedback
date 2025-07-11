"""
Tests para los validadores
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.validators import validate_rating, validate_phone_number, validate_place_name, validate_review_text

def test_validate_rating():
    """Test para validación de calificaciones"""
    
    # Tests válidos
    assert validate_rating(1) == (True, 1)
    assert validate_rating(5) == (True, 5)
    assert validate_rating("3") == (True, 3)
    
    # Tests inválidos
    assert validate_rating(0) == (False, "La calificación debe estar entre 1 y 5")
    assert validate_rating(6) == (False, "La calificación debe estar entre 1 y 5")
    assert validate_rating("abc") == (False, "La calificación debe ser un número del 1 al 5")

def test_validate_phone_number():
    """Test para validación de números de teléfono"""
    
    # Tests válidos
    assert validate_phone_number("+1234567890") == (True, "+1234567890")
    assert validate_phone_number("1234567890") == (True, "+1234567890")
    assert validate_phone_number("+1 (234) 567-890") == (True, "+1234567890")
    
    # Tests inválidos
    assert validate_phone_number("123") == (False, "El número de teléfono es demasiado corto")
    assert validate_phone_number("abc123") == (False, "El número de teléfono contiene caracteres inválidos")

def test_validate_place_name():
    """Test para validación de nombres de lugares"""
    
    # Tests válidos
    assert validate_place_name("Restaurante ABC") == (True, "Restaurante ABC")
    assert validate_place_name("  Café XYZ  ") == (True, "Café XYZ")
    
    # Tests inválidos
    assert validate_place_name("") == (False, "El nombre del lugar no puede estar vacío")
    assert validate_place_name("A") == (False, "El nombre del lugar es demasiado corto")

def test_validate_review_text():
    """Test para validación de texto de reseñas"""
    
    # Tests válidos
    valid_text = "Excelente servicio y comida deliciosa. Muy recomendado!"
    assert validate_review_text(valid_text) == (True, valid_text)
    
    # Tests inválidos
    assert validate_review_text("") == (False, "El texto de la reseña no puede estar vacío")
    assert validate_review_text("Bueno") == (False, "La reseña debe tener al menos 10 caracteres")

if __name__ == "__main__":
    print("🧪 Ejecutando tests de validadores...")
    
    test_validate_rating()
    test_validate_phone_number()
    test_validate_place_name()
    test_validate_review_text()
    
    print("✅ Todos los tests pasaron!") 