# Implementación de Validación de Datos

## Cambios realizados

### 1. **Nuevo archivo: `validators.py`**
Módulo centralizado para validación de datos con funciones reutilizables:

- **`validar_email(email)`** - Valida formato de email
- **`validar_contraseña(contraseña)`** - Valida que la contraseña sea fuerte:
  - Mínimo 8 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un número
  - Al menos un carácter especial (!@#$%^&*)
- **`validar_username(username)`** - Valida el usuario:
  - 3-50 caracteres
  - Solo letras, números, guiones y guiones bajos
- **`validar_registro(username, email, contraseña)`** - Valida el registro completo

### 2. **Actualización: `routes/auth.py`**
Mejoras de seguridad en las rutas de autenticación:

#### Registro (`/registro`)
- ✅ Valida email con formato correcto
- ✅ Valida contraseña fuerte
- ✅ Verifica que las contraseñas coincidan
- ✅ Mejor manejo de errores con try/except
- ✅ Logging de eventos (registro exitoso, errores)
- ✅ Mensajes de error específicos para cada validación

#### Login (`/login`)
- ✅ Validación de campos obligatorios
- ✅ Mejor manejo de errores
- ✅ Logging de intentos (exitosos y fallidos)
- ✅ Mensajes genéricos de error (por seguridad)

#### Recuperación (`/recuperar`)
- ✅ Valida que el email tenga formato correcto
- ✅ No revela si el email existe (previene phishing)
- ✅ Logging de intentos
- ✅ Mejor manejo de excepciones

#### Restablecer (`/restablecer/<token>`)
- ✅ Valida contraseña fuerte con los mismos requisitos
- ✅ Verifica que las contraseñas coincidan
- ✅ Better error handling with logging
- ✅ Manejo robusto de excepciones

#### 2FA (`/login/2fa`)
- ✅ Validación de código obligatorio
- ✅ Logging de eventos
- ✅ Better error handling

### 3. **Actualización: `app.py`**
Configuración de logging centralizado:
- ✅ Logging automático de eventos importantes
- ✅ Archivos de log rotativos (máx 10MB por archivo)
- ✅ Almacenamiento en carpeta `logs/`
- ✅ Timestamps y contexto en cada log

### 4. **Nuevo archivo: `tests_validators.py`**
Suite de tests unitarios para validadores:

Ejecutar tests:
```bash
source venv/bin/activate
pip install pytest
python -m pytest tests_validators.py -v
```

Incluye tests para:
- Emails válidos e inválidos
- Contraseñas fuertes y débiles
- Usernames válidos e inválidos
- Registro completo

## Requisitos de seguridad

### Contraseña
```
Antes:  Mínimo 6 caracteres
Ahora:  Mínimo 8 caracteres + mayúscula + minúscula + número + símbolo
```

### Email
- Validación de formato RFC 5322 simplificado
- Máximo 120 caracteres

### Usuario
- 3-50 caracteres
- Solo alfanuméricos, guiones y guiones bajos

## Mejoras de seguridad

1. **Validación robusta** - Todos los inputs se validan
2. **Mensajes de error específicos** - Ayuda al usuario
3. **Mensajes genéricos en login** - No revela qué falló (seguridad)
4. **Logging completo** - Auditoría de eventos
5. **Manejo de excepciones** - No expone internals
6. **Confirmación de contraseña** - En registro y recuperación

## Uso de validadores en código

```python
from validators import validar_email, validar_contraseña, validar_registro

# Validar email
email_valido, error = validar_email('usuario@example.com')
if not email_valido:
    flash(error, 'error')

# Validar contraseña
contraseña_valida, error = validar_contraseña('MiPass123!')
if not contraseña_valida:
    flash(error, 'error')

# Validar registro completo
resultado = validar_registro(username, email, password)
if not resultado['valido']:
    for error in resultado['errores']:
        flash(error, 'error')
```

## Próximos pasos recomendados

1. **Rate Limiting** - Limitar intentos de login/registro
2. **CAPTCHA** - Proteger contra bots
3. **Verificación de email** - Confirmar email antes de usar
4. **Password hasher mejorado** - Usar Argon2 en lugar de werkzeug
5. **Auditoría más detallada** - Guardar IP, dispositivo, etc.
6. **2FA para email** - Enviar códigos por email también
