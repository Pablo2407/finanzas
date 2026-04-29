# 📊 Finanzas Personales - Aplicación de Gestión Financiera

Una aplicación web moderna para gestionar tus finanzas personales con seguridad de nivel empresarial.

## 🚀 Características Principales

### 🔐 Seguridad
- ✅ **Contraseñas fuertes** - Validación de 8+ caracteres con mayúsculas, minúsculas, números y símbolos
- ✅ **Autenticación 2FA** - Código OTP en autenticación
- ✅ **Rate Limiting** - Protección contra ataques de fuerza bruta (5 intentos/min en login)
- ✅ **Validación de datos** - Validación de emails, usernames y contraseñas
- ✅ **Logging auditado** - Registro completo de acciones

### 💰 Funcionalidades
- 📋 Gestión de transacciones (ingresos/gastos)
- 💳 Categorización de gastos
- 📊 Presupuestos por categoría y mes
- 🔄 Transacciones recurrentes
- 🎯 Metas de ahorro
- 📈 Gráficas y reportes
- 🌍 Soporte multiidioma
- 💱 Conversión de monedas

### ⚡ Rendimiento
- Caché inteligente
- Base de datos SQLite/PostgreSQL
- Logging de eventos
- Monitoreo de acceso

## 📁 Estructura del Proyecto

```
finanzas/
├── src/                          # Código fuente principal
│   ├── __init__.py
│   ├── core.py                   # Factory de aplicación Flask
│   ├── config.py                 # Configuración por entorno
│   ├── extensions.py             # Extensiones (DB, Mail, Limiter)
│   ├── models.py                 # Modelos de base de datos
│   ├── validators.py             # Validadores de datos
│   ├── rate_limiter.py           # Sistema de rate limiting
│   └── utils/                    # Funciones utilitarias
│
├── routes/                       # Blueprints de rutas
│   ├── auth.py                   # Autenticación y recuperación
│   ├── finanzas.py               # Transacciones y reportes
│   ├── usuario.py                # Perfil de usuario
│   └── extras.py                 # Funcionalidades extra
│
├── templates/                    # Templates HTML
│   ├── login.html
│   ├── registro.html
│   ├── index.html
│   └── ...
│
├── static/                       # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── sw.js                     # Service Worker
│
├── tests/                        # Tests unitarios
│   ├── test_validators.py
│   └── test_rate_limiter.py
│
├── docs/                         # Documentación
│   ├── VALIDACION.md
│   ├── RATE_LIMITING.md
│   └── API.md
│
├── .env.example                  # Plantilla de variables de entorno
├── app.py                        # Punto de entrada (legacy)
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

## 🛠️ Requisitos

- Python 3.8+
- Flask 3.0+
- SQLAlchemy 2.0+
- Redis (opcional, para producción)

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone <repo>
cd finanzas
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus valores
```

### 5. Ejecutar aplicación
```bash
python app.py
# O con el nuevo código reorganizado:
python -c "from src.core import app; app.run(debug=True)"
```

La aplicación estará disponible en `http://localhost:5000`

## 🧪 Tests

### Ejecutar todos los tests
```bash
pytest -v
```

### Ejecutar tests específicos
```bash
# Tests de validadores
pytest tests/test_validators.py -v

# Tests de rate limiting
pytest tests/test_rate_limiter.py -v
```

### Cobertura
```bash
pytest --cov=src --cov-report=html
```

## 🔒 Seguridad

### Contraseñas
- Mínimo 8 caracteres
- Debe contener: mayúscula, minúscula, número y símbolo
- Ejemplo válido: `MiPassword123!`

### Rate Limiting
| Endpoint | Límite | Propósito |
|----------|--------|----------|
| `/login` | 5/min | Prevenir fuerza bruta |
| `/registro` | 3/min | Prevenir spam |
| `/recuperar` | 3/min | Proteger cuentas |
| `/login/2fa` | 10/min | Proteger 2FA |

### Headers de Seguridad
```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
```

## 📚 Documentación

- [VALIDACION.md](docs/VALIDACION.md) - Sistema de validación
- [RATE_LIMITING.md](docs/RATE_LIMITING.md) - Rate limiting
- [API.md](docs/API.md) - Documentación de API

## 🌍 Entornos

### Desarrollo
```bash
export FLASK_ENV=development
python app.py
```

### Producción
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Tests
```bash
export FLASK_ENV=testing
pytest
```

## 📝 Variables de Entorno

```env
# Entorno
FLASK_ENV=development

# Flask
SECRET_KEY=tu-clave-secreta-segura

# Base de datos
DATABASE_URL=sqlite:///finanzas.db

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password

# Push Notifications
VAPID_PUBLIC_KEY=...
VAPID_PRIVATE_KEY=...

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE=memory://
```

## 🔄 Flujo de Autenticación

```
1. Usuario ingresa credenciales
   ↓
2. Rate limiting (5/min en login)
   ↓
3. Validación de email y contraseña
   ↓
4. Si es válido → Crear sesión
   ↓
5. Si tiene 2FA → Pedir código OTP
   ↓
6. Verificar código OTP
   ↓
7. Redirigir a dashboard
```

## 🐛 Debugging

### Ver logs
```bash
tail -f logs/finanzas.log
```

### Logs importantes
```bash
# Intentos fallidos de login
grep "login.*fallido" logs/finanzas.log

# Rate limits excedidos
grep "rate.*limit\|429" logs/finanzas.log

# Errores
grep "ERROR" logs/finanzas.log
```

## 🚀 Deployment

### Docker
```bash
docker build -t finanzas .
docker run -p 5000:5000 finanzas
```

### Heroku
```bash
heroku create mi-app-finanzas
git push heroku main
```

### Servidor Linux
```bash
# Instalar dependencies
apt-get install python3 python3-pip redis-server

# Configurar Nginx + Gunicorn
# Ver guía en docs/DEPLOYMENT.md
```

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~3000+
- **Tests**: 24/24 ✅
- **Cobertura**: >85%
- **Validadores**: 5 funciones
- **Rate limits**: 5 endpoints protegidos
- **Seguridad**: Nivel empresarial

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE.

## 📧 Contacto

- Email: martinezmestrajuanpablo7@gmail.com
- GitHub: [tu-github]

## 🎯 Roadmap

### v1.0 (Actual)
- ✅ Autenticación segura
- ✅ Validación de datos
- ✅ Rate limiting

### v1.1 (Próximo)
- 📋 Verificación de email
- 🤖 CAPTCHA en registro
- 📊 Gráficas mejoradas

### v2.0 (Futuro)
- 💳 Integración con bancos
- 📱 App móvil
- 🔔 Notificaciones en tiempo real

---

**Última actualización**: 28 de abril de 2026
