"""
Core de la aplicación Flask
"""
from flask import Flask, render_template
from .config import get_config
from .extensions import db, login_manager, mail, limiter
from .models import Usuario
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """Configurar logging de la aplicación"""
    if not app.debug:
        # Crear carpeta de logs si no existe
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar rotating file handler
        file_handler = RotatingFileHandler('logs/finanzas.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [en %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicación de finanzas iniciada')


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(get_config())

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    limiter.init_app(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Manejador de errores de rate limiting
    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f'Rate limit excedido: {e.description}')
        return render_template('rate_limit_error.html', error=str(e.description)), 429

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.context_processor
    def inject_moneda():
        from flask_login import current_user
        if current_user and current_user.is_authenticated:
            return dict(moneda=current_user.moneda)
        return dict(moneda='$')

    # Registrar blueprints
    from ..routes.auth import auth
    from ..routes.finanzas import finanzas
    from ..routes.usuario import usuario
    from ..routes.extras import extras
    
    app.register_blueprint(auth)
    app.register_blueprint(finanzas)
    app.register_blueprint(usuario)
    app.register_blueprint(extras)

    # Crear tablas de BD
    with app.app_context():
        db.create_all()
    
    # Ruta de landing
    @app.route('/landing')
    def landing():
        return render_template('landing.html')

    return app


# Crear instancia de la aplicación
app = create_app()
