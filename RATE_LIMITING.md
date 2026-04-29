# Rate Limiting - Protección contra ataques de fuerza bruta

## ¿Qué es Rate Limiting?

Rate Limiting es una técnica de seguridad que limita el número de solicitudes que un usuario o IP puede realizar en un período de tiempo específico. Esto protege contra:

- **Ataques de fuerza bruta** en login
- **Spam** de registros
- **Abuso** de API
- **Enumeración** de usuarios válidos

## Implementación en el Proyecto

### Archivos modificados/creados:

1. **`extensions.py`** - Inicialización de Flask-Limiter
2. **`rate_limiter.py`** - Configuración personalizada de límites
3. **`app.py`** - Inicialización y manejador de errores 429
4. **`routes/auth.py`** - Aplicación de límites a rutas sensibles
5. **`templates/rate_limit_error.html`** - Página de error amigable

## Límites Configurados

| Ruta | Límite | Propósito |
|------|--------|----------|
| `/login` | 5 por minuto | Protege contra fuerza bruta |
| `/registro` | 3 por minuto | Previene spam de registros |
| `/recuperar` | 3 por minuto | Protege contra abuso |
| `/login/2fa` | 10 por minuto | Protege verificación 2FA |
| Defecto | 50 por hora | Límite general |

## Cómo funciona

### 1. Identificación de cliente
Por defecto usa la **dirección IP** del cliente. En producción con proxies, configurar:

```python
# En config.py
X_FORWARDED_FOR = True  # Si está detrás de un proxy
```

### 2. Almacenamiento
- **Desarrollo**: Memoria (en RAM)
- **Producción**: Redis recomendado

```python
# Para producción con Redis:
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
```

### 3. Respuesta al límite excedido
- Status HTTP: **429 Too Many Requests**
- Headers agregados:
  - `RateLimit-Limit`: límite total
  - `RateLimit-Remaining`: intentos restantes
  - `RateLimit-Reset`: cuándo se reinicia

## Código de ejemplo

### Aplicar a una ruta personalizada

```python
from extensions import limiter

@app.route('/api/endpoint', methods=['POST'])
@limiter.limit("10 per minute")  # 10 requests por minuto
def my_endpoint():
    return "Success", 200
```

### Usar función auxiliar

```python
from rate_limiter import aplicar_rate_limit, RATE_LIMITS

@auth.route('/mi-ruta', methods=['POST'])
@aplicar_rate_limit('login')  # Usa el límite de 'login'
def mi_ruta():
    return "OK"
```

## Testing

Ejecutar tests de rate limiting:

```bash
source venv/bin/activate
python -m pytest tests_rate_limiter.py -v
```

Para pruebas en desarrollo, el rate limiting se respeta pero puede ser más flexible.

## Monitoreo y Logging

Cuando se excede un límite:

1. Se registra en logs
2. Usuario ve página 429
3. IP se rastrea en los logs

Ver logs:
```bash
tail -f logs/finanzas.log | grep "rate"
```

## Configuración en Producción

### Con Redis (recomendado):

1. Instalar Redis:
```bash
pip install redis
```

2. Actualizar `extensions.py`:
```python
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
```

3. Iniciar Redis:
```bash
redis-server
```

### Variables de entorno recomendadas:

```env
# .env
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE=redis://localhost:6379
```

## Manejo de errores

La aplicación maneja automáticamente errores 429 con:

1. **Template personalizado**: `templates/rate_limit_error.html`
2. **Logging** de intentos bloqueados
3. **Headers** estándar HTTP

## Bypass de rate limiting (admin)

Para endpoints administrativos, excluir del rate limiting:

```python
@app.route('/admin/dashboard')
@limiter.exempt  # No aplicar rate limit
def admin_dashboard():
    return "Admin area"
```

## Seguridad adicional

### Combinado con validación:
- ✅ Rate limiting: límite de requests
- ✅ Validación: formato de datos
- ✅ Captcha: (futuro)
- ✅ Verificación email: (futuro)

### Registros de seguridad:
```bash
# Ver intentos bloqueados
grep "rate.*limit" logs/finanzas.log

# Ver intentos fallidos de login
grep "login.*fallido" logs/finanzas.log
```

## Próximos pasos

1. **Implementar verificación de email**
2. **Agregar CAPTCHA** para registros
3. **Configurar Redis** para producción
4. **Dashboard de monitoreo** de intentos bloqueados
5. **IP whitelist** para personal confiable
