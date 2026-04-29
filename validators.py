"""
Validadores para la aplicación
"""
import re
from typing import Tuple


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida que el email tenga formato correcto
    
    Args:
        email: Email a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not email or not isinstance(email, str):
        return False, "El email es requerido"
    
    email = email.strip()
    
    # Expresión regular para validar email
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(patron_email, email):
        return False, "El email no tiene un formato válido"
    
    if len(email) > 120:
        return False, "El email es demasiado largo"
    
    return True, ""


def validar_contraseña(contraseña: str) -> Tuple[bool, str]:
    """
    Valida que la contraseña sea fuerte:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    
    Args:
        contraseña: Contraseña a validar
        
    Returns:
        Tupla (es_valida, mensaje_error)
    """
    if not contraseña or not isinstance(contraseña, str):
        return False, "La contraseña es requerida"
    
    if len(contraseña) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(contraseña) > 128:
        return False, "La contraseña es demasiado larga"
    
    # Validar que tenga mayúscula
    if not re.search(r'[A-Z]', contraseña):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    # Validar que tenga minúscula
    if not re.search(r'[a-z]', contraseña):
        return False, "La contraseña debe contener al menos una minúscula"
    
    # Validar que tenga número
    if not re.search(r'\d', contraseña):
        return False, "La contraseña debe contener al menos un número"
    
    # Validar que tenga carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
        return False, "La contraseña debe contener al menos un carácter especial (!@#$%^&*)"
    
    return True, ""


def validar_username(username: str) -> Tuple[bool, str]:
    """
    Valida que el username sea válido:
    - Mínimo 3 caracteres
    - Máximo 50 caracteres
    - Solo letras, números y guiones bajos
    
    Args:
        username: Usuario a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not username or not isinstance(username, str):
        return False, "El usuario es requerido"
    
    username = username.strip()
    
    if len(username) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    
    if len(username) > 50:
        return False, "El usuario es demasiado largo"
    
    # Solo letras, números y guiones bajos
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "El usuario solo puede contener letras, números, guiones y guiones bajos"
    
    return True, ""


def validar_registro(username: str, email: str, contraseña: str) -> dict:
    """
    Valida todos los campos del registro
    
    Args:
        username: Usuario
        email: Email
        contraseña: Contraseña
        
    Returns:
        Dict con estructura: {'valido': bool, 'errores': [lista de errores]}
    """
    errores = []
    
    # Validar username
    username_valido, err_username = validar_username(username)
    if not username_valido:
        errores.append(err_username)
    
    # Validar email
    email_valido, err_email = validar_email(email)
    if not email_valido:
        errores.append(err_email)
    
    # Validar contraseña
    contraseña_valida, err_contraseña = validar_contraseña(contraseña)
    if not contraseña_valida:
        errores.append(err_contraseña)
    
    return {
        'valido': len(errores) == 0,
        'errores': errores
    }
