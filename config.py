import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///finanzas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Push Notifications (VAPID)
    VAPID_PUBLIC_KEY = os.getenv('VAPID_PUBLIC_KEY')
    VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY')
    VAPID_CLAIM_EMAIL = os.getenv('VAPID_CLAIM_EMAIL')
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_STORAGE = os.getenv('RATELIMIT_STORAGE', 'memory://')
    RATELIMIT_DEFAULT = '200 per day'


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    RATELIMIT_ENABLED = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    RATELIMIT_STORAGE = os.getenv('RATELIMIT_STORAGE', 'redis://localhost:6379')


class TestingConfig(Config):
    """Configuración para pruebas"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE = 'memory://'


def get_config():
    """Retorna la configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
