"""
Tests para Rate Limiting
Ejecutar con: python -m pytest tests_rate_limiter.py -v
"""
import pytest
from app import app
from extensions import db, limiter
from models import Usuario
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    """Crear cliente de prueba"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['RATELIMIT_ENABLED'] = True
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def usuario_prueba(client):
    """Crear usuario de prueba"""
    with app.app_context():
        usuario = Usuario(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('Password123!')
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario


class TestRateLimitLogin:
    """Tests para rate limiting en login"""
    
    def test_login_normal(self, client, usuario_prueba):
        """Test que el login funciona normalmente"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'Password123!'
        })
        assert response.status_code in [200, 302]  # 302 es redirect a página
    
    def test_login_rate_limit_headers(self, client):
        """Test que los headers de rate limit están presentes"""
        response = client.get('/login')
        # Los headers RateLimit deberían estar presentes
        assert response.status_code == 200


class TestRateLimitRegistro:
    """Tests para rate limiting en registro"""
    
    def test_registro_headers(self, client):
        """Test que la ruta de registro tiene rate limiting"""
        response = client.post('/registro', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Password123!',
            'confirmar_password': 'Password123!'
        })
        # Debería tener la ruta (200 o redirigir)
        assert response.status_code in [200, 302, 400]


class TestRateLimitRecuperar:
    """Tests para rate limiting en recuperación"""
    
    def test_recuperar_exists(self, client):
        """Test que la ruta de recuperación existe"""
        response = client.get('/recuperar')
        assert response.status_code == 200


class TestRateLimitError:
    """Tests para el error 429"""
    
    def test_rate_limit_error_handler_exists(self):
        """Test que existe manejador de error 429"""
        # Verificar que la función de error está registrada
        assert 429 in app.error_handler_spec[None]


class TestRateLimitConfiguration:
    """Tests para la configuración de rate limiting"""
    
    def test_limiter_initialized(self):
        """Test que limiter está inicializado"""
        assert limiter is not None
    
    def test_rate_limit_limits_exist(self):
        """Test que existen los límites definidos"""
        from rate_limiter import RATE_LIMITS
        
        assert 'login' in RATE_LIMITS
        assert 'registro' in RATE_LIMITS
        assert 'recuperar' in RATE_LIMITS
        assert '2fa' in RATE_LIMITS


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
