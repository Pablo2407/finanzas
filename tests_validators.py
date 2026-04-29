"""
Tests para los validadores
Ejecutar con: python -m pytest tests_validators.py -v
"""
import pytest
from validators import validar_email, validar_contraseña, validar_username, validar_registro


class TestValidarEmail:
    """Tests para validación de emails"""
    
    def test_email_valido(self):
        valido, msg = validar_email('usuario@example.com')
        assert valido is True
        assert msg == ""
    
    def test_email_sin_formato(self):
        valido, msg = validar_email('usuario@')
        assert valido is False
        assert "formato" in msg.lower()
    
    def test_email_sin_dominio(self):
        valido, msg = validar_email('usuario')
        assert valido is False
    
    def test_email_vacio(self):
        valido, msg = validar_email('')
        assert valido is False
        assert "requerido" in msg.lower()


class TestValidarContraseña:
    """Tests para validación de contraseñas"""
    
    def test_contraseña_fuerte(self):
        valido, msg = validar_contraseña('MiPassword123!')
        assert valido is True
        assert msg == ""
    
    def test_contraseña_sin_mayuscula(self):
        valido, msg = validar_contraseña('mipassword123!')
        assert valido is False
        assert "mayúscula" in msg.lower()
    
    def test_contraseña_sin_minuscula(self):
        valido, msg = validar_contraseña('MIPASSWORD123!')
        assert valido is False
        assert "minúscula" in msg.lower()
    
    def test_contraseña_sin_numero(self):
        valido, msg = validar_contraseña('MiPassword!')
        assert valido is False
        assert "número" in msg.lower()
    
    def test_contraseña_sin_especial(self):
        valido, msg = validar_contraseña('MiPassword123')
        assert valido is False
        assert "especial" in msg.lower()
    
    def test_contraseña_muy_corta(self):
        valido, msg = validar_contraseña('Pass1!')
        assert valido is False
        assert "8 caracteres" in msg
    
    def test_contraseña_vacia(self):
        valido, msg = validar_contraseña('')
        assert valido is False
        assert "requerid" in msg.lower()  # Detecta "requerida" o "requerido"


class TestValidarUsername:
    """Tests para validación de usuarios"""
    
    def test_username_valido(self):
        valido, msg = validar_username('usuario123')
        assert valido is True
        assert msg == ""
    
    def test_username_muy_corto(self):
        valido, msg = validar_username('ab')
        assert valido is False
        assert "3 caracteres" in msg
    
    def test_username_con_caracteres_invalidos(self):
        valido, msg = validar_username('usuario@123')
        assert valido is False
        assert "solo puede contener" in msg.lower()
    
    def test_username_vacio(self):
        valido, msg = validar_username('')
        assert valido is False
        assert "requerido" in msg.lower()


class TestValidarRegistro:
    """Tests para validación completa de registro"""
    
    def test_registro_valido(self):
        resultado = validar_registro('usuario123', 'usuario@example.com', 'MiPassword123!')
        assert resultado['valido'] is True
        assert len(resultado['errores']) == 0
    
    def test_registro_con_errores(self):
        resultado = validar_registro('ab', 'email-invalido', 'weak')
        assert resultado['valido'] is False
        assert len(resultado['errores']) > 0
        assert any('usuario' in e.lower() for e in resultado['errores'])
        assert any('formato' in e.lower() for e in resultado['errores'])
        assert any('contraseña' in e.lower() for e in resultado['errores'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
