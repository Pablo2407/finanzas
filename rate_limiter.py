"""
Sistema de Rate Limiting para proteger contra ataques de fuerza bruta
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
import logging

logger = logging.getLogger(__name__)

# Inicializar Limiter - se configura en app.py
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # En producción usar Redis
)

# Límites específicos para diferentes endpoints
RATE_LIMITS = {
    # Autenticación - muy estricto
    'login': '5 per minute',           # 5 intentos por minuto
    'registro': '5 per minute',        # 5 registros por minuto
    'recuperar': '5 per minute',       # 5 recuperaciones por minuto
    '2fa': '10 per minute',            # 10 intentos 2FA por minuto
    
    # API - moderado
    'api_general': '30 per minute',    # 30 por minuto general
    
    # Endpoints públicos - permisivo
    'publico': '100 per hour',         # 100 por hora
}

def aplicar_rate_limit(limite_clave):
    """
    Decorator para aplicar rate limiting a una ruta
    
    Uso:
        @auth.route('/login', methods=['POST'])
        @aplicar_rate_limit('login')
        def login():
            ...
    """
    def decorator(f):
        limite = RATE_LIMITS.get(limite_clave, '50 per minute')
        return limiter.limit(limite)(f)
    return decorator

def obtener_limite_info(limite_clave):
    """Obtiene información legible del límite"""
    return RATE_LIMITS.get(limite_clave, 'Límite por defecto')

def log_rate_limit_exceeded(endpoint, ip):
    """Registra cuando se excede el rate limit (para auditoría)"""
    logger.warning(f'Rate limit exceeded para endpoint {endpoint} desde IP {ip}')
