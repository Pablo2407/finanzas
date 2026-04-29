# 📁 Estructura del Proyecto - Finanzas

## Vista General

```
finanzas/
│
├── 📄 ARCHIVOS RAÍZ (Punto de entrada)
│   ├── app.py                    # Punto de entrada LEGACY (mantener por compatibilidad)
│   ├── app_new.py                # Punto de entrada NUEVO
│   ├── requirements.txt           # Dependencias del proyecto
│   └── Procfile                  # Configuración para Heroku
│
├── 📁 src/ (Código fuente reorganizado - NUEVO)
│   ├── __init__.py               # Paquete Python
│   ├── core.py                   # Factory de aplicación Flask
│   ├── config.py                 # Configuración por entorno
│   ├── extensions.py             # Extensiones (DB, Mail, Limiter)
│   ├── models.py                 # Modelos de base de datos
│   ├── validators.py             # Validadores de datos
│   ├── rate_limiter.py           # Sistema de rate limiting
│   └── utils/                    # Funciones utilitarias
│       ├── __init__.py
│       ├── helpers.py            # Funciones helper generales
│       └── email.py              # Funciones de email
│
├── 📁 routes/ (Blueprints - Rutas y controladores)
│   ├── __init__.py
│   ├── auth.py                   # Rutas de autenticación
│   ├── finanzas.py               # Rutas de finanzas
│   ├── usuario.py                # Rutas de perfil de usuario
│   └── extras.py                 # Rutas extras
│
├── 📁 templates/ (HTML - Vistas)
│   ├── base.html                 # Template base (herencia)
│   ├── login.html                # Login
│   ├── registro.html             # Registro
│   ├── 2fa_login.html            # Verificación 2FA en login
│   ├── 2fa_activar.html          # Activar 2FA
│   ├── index.html                # Dashboard principal
│   ├── perfil.html               # Perfil de usuario
│   ├── rate_limit_error.html    # Error 429 (rate limit)
│   └── ...otros templates
│
├── 📁 static/ (Archivos estáticos)
│   ├── css/                      # Estilos CSS
│   ├── js/                       # Scripts JavaScript
│   ├── img/                      # Imágenes
│   ├── manifest.json             # Manifiesto PWA
│   └── sw.js                     # Service Worker (PWA)
│
├── 📁 tests/ (Tests unitarios - REORGANIZADO)
│   ├── __init__.py
│   ├── test_validators.py        # Tests de validadores (17 tests)
│   ├── test_rate_limiter.py      # Tests de rate limiting (7 tests)
│   ├── test_auth.py              # Tests de autenticación (futuro)
│   └── conftest.py               # Fixtures de pytest (futuro)
│
├── 📁 docs/ (Documentación)
│   ├── README.md                 # Guía principal del proyecto
│   ├── VALIDACION.md             # Documentación de validadores
│   ├── RATE_LIMITING.md          # Documentación de rate limiting
│   ├── API.md                    # Documentación de API
│   ├── DEPLOYMENT.md             # Guía de deployment
│   ├── CONTRIBUTING.md           # Guía para contribuidores
│   └── ARCHITECTURE.md           # Arquitectura del sistema
│
├── 📁 config/ (Configuración adicional)
│   ├── logging.yaml              # Configuración de logging
│   └── nginx.conf                # Configuración Nginx (producción)
│
├── 📁 .github/ (GitHub específico)
│   ├── workflows/                # CI/CD workflows
│   └── ISSUE_TEMPLATE/           # Plantillas de issues
│
├── 📁 instance/ (Archivos de instancia - NO VERSIONADO)
│   ├── finanzas.db               # Base de datos SQLite
│   └── ...otros archivos runtime
│
├── 📁 logs/ (Logs de aplicación - NO VERSIONADO)
│   └── finanzas.log              # Log principal
│
├── 📁 venv/ (Entorno virtual - NO VERSIONADO)
│   └── ...archivos virtuales
│
├── 🔧 ARCHIVOS DE CONFIGURACIÓN
│   ├── .env                      # Variables de entorno (NO VERSIONADO)
│   ├── .env.example              # Plantilla de .env
│   ├── .gitignore                # Archivos a ignorar en git
│   ├── .flake8                   # Configuración de linting
│   ├── pytest.ini                # Configuración de pytest
│   ├── setup.py                  # Configuración de instalación (futuro)
│   └── docker-compose.yml        # Docker compose (futuro)
│
└── 📋 DOCUMENTACIÓN
    ├── README.md                 # Guía principal
    ├── README_NUEVO.md           # Nueva guía (con estructura)
    ├── VALIDACION.md             # Validación de datos
    ├── RATE_LIMITING.md          # Rate limiting
    ├── IMPLEMENTACION_RATE_LIMITING.md  # Resumen implementación
    ├── LICENSE                   # Licencia MIT
    └── CHANGELOG.md              # Historial de cambios
```

## 📊 Distribución de Archivos

### Por tipo:
- **Python**: src/, routes/, tests/, *.py
- **HTML**: templates/
- **CSS/JS**: static/
- **Config**: .env, config.py, config/
- **Docs**: docs/, *.md

### Por tamaño:
- **Grandes**: models.py, routes/finanzas.py (lógica compleja)
- **Medianos**: validators.py, rate_limiter.py (funciones auxiliares)
- **Pequeños**: __init__.py, helpers (módulos específicos)

## 🔄 Flujo de Importes

### Viejo (Legacy)
```python
# app.py importa directamente de raíz
from extensions import db
from models import Usuario
from routes.auth import auth
```

### Nuevo (Reorganizado)
```python
# src/core.py importa de forma relativa
from .extensions import db
from .models import Usuario
from ..routes.auth import auth
```

## 🚀 Cómo ejecutar

### Viejo (Legacy)
```bash
python app.py
```

### Nuevo (Recomendado)
```bash
python app_new.py
# O
python -c "from src.core import app; app.run()"
```

## 📈 Mejoras de esta estructura

✅ **Escalabilidad** - Fácil agregar nuevas funcionalidades
✅ **Mantenibilidad** - Código organizado por responsabilidad
✅ **Claridad** - Directorios con propósito claro
✅ **Profesionalismo** - Estructura de proyecto grande
✅ **Separación** - Tests, docs, código separados
✅ **Configuración** - Config centralizada por entorno

## 🔐 Archivos NO versionados (.gitignore)

```
venv/              # Entorno virtual
*.pyc              # Archivos compilados
__pycache__/       # Caché de Python
.env               # Variables de entorno
instance/          # Base de datos
logs/              # Logs
.pytest_cache/     # Caché pytest
.coverage          # Cobertura
*.db               # Base de datos SQLite
```

## 📚 Próximos pasos

- [ ] Mover código legacy a nueva estructura
- [ ] Actualizar imports en routes/
- [ ] Reorganizar tests
- [ ] Agregar CI/CD (GitHub Actions)
- [ ] Agregar Docker
- [ ] Documentar API completa
