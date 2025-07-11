import re
from typing import Union, Tuple

def validate_rating(rating: Union[str, int]) -> Tuple[bool, Union[int, str]]:
    """
    Validar calificación de 1 a 5 estrellas
    
    Args:
        rating: Calificación como string o int
        
    Returns:
        Tuple[bool, Union[int, str]]: (es_válido, rating_int_o_error_message)
    """
    try:
        rating_int = int(rating)
        if 1 <= rating_int <= 5:
            return True, rating_int
        else:
            return False, "La calificación debe estar entre 1 y 5"
    except (ValueError, TypeError):
        return False, "La calificación debe ser un número del 1 al 5"

def validate_phone_number(phone: str) -> Tuple[bool, Union[str, str]]:
    """
    Validar formato de número de teléfono
    
    Args:
        phone: Número de teléfono como string
        
    Returns:
        Tuple[bool, Union[str, str]]: (es_válido, número_limpio_o_error_message)
    """
    # Remover espacios, guiones y paréntesis
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Verificar que solo contenga dígitos y +
    if not re.match(r'^\+?[\d]+$', cleaned):
        return False, "El número de teléfono contiene caracteres inválidos"
    
    # Verificar longitud mínima
    if len(cleaned) < 10:
        return False, "El número de teléfono es demasiado corto"
    
    # Agregar + si no está presente
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    return True, cleaned

def validate_place_name(place_name: str) -> Tuple[bool, Union[str, str]]:
    """
    Validar nombre del lugar
    
    Args:
        place_name: Nombre del lugar
        
    Returns:
        Tuple[bool, Union[str, str]]: (es_válido, nombre_limpio_o_error_message)
    """
    if not place_name or not place_name.strip():
        return False, "El nombre del lugar no puede estar vacío"
    
    cleaned = place_name.strip()
    
    if len(cleaned) < 2:
        return False, "El nombre del lugar es demasiado corto"
    
    if len(cleaned) > 100:
        return False, "El nombre del lugar es demasiado largo"
    
    return True, cleaned

def validate_review_text(text: str) -> Tuple[bool, Union[str, str]]:
    """
    Validar texto de la reseña
    
    Args:
        text: Texto de la reseña
        
    Returns:
        Tuple[bool, Union[str, str]]: (es_válido, texto_limpio_o_error_message)
    """
    if not text or not text.strip():
        return False, "El texto de la reseña no puede estar vacío"
    
    cleaned = text.strip()
    
    if len(cleaned) < 10:
        return False, "La reseña debe tener al menos 10 caracteres"
    
    if len(cleaned) > 1000:
        return False, "La reseña es demasiado larga (máximo 1000 caracteres)"
    
    return True, cleaned 