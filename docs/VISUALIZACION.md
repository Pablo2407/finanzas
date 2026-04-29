# 📊 Estructura Visual del Proyecto Reorganizado

## Árbol del Proyecto

```
finanzas/ (raíz del proyecto)
│
├── 🗂️ CÓDIGO FUENTE
├── ├── src/                      ⭐ NUEVO - Código principal
│   ├── __init__.py
│   ├── core.py                   ← Factory de aplicación
│   ├── config.py                 ← Configuración por entorno
│   ├── extensions.py             ← Extensiones (DB, Mail, Limiter)
│   ├── models.py                 ← Modelos de BD
│   ├── validators.py             ← Validadores de datos
│   ├── rate_limiter.py           ← Sistema de rate limiting
│   └── utils/                    ← Funciones auxiliares
│       ├── __init__.py
│       ├── helpers.py            (futuro)
│       └── email.py              (futuro)
│
├── routes/                       ← Blueprints de rutas
│   ├── __init__.py
│   ├── auth.py                   ← Autenticación
│   ├── finanzas.py               ← Finanzas
│   ├── usuario.py                ← Perfil de usuario
│   └── extras.py                 ← Extras
│
├── 🗂️ TESTS
├── ├── tests/                    ⭐ NUEVO - Tests organizados
│   ├── __init__.py
│   ├── test_validators.py        ← 17 tests ✅
│   ├── test_rate_limiter.py      ← 7 tests ✅
│   ├── conftest.py               (futuro)
│   └── fixtures.py               (futuro)
│
├── 🗂️ INTERFAZ
├── ├── templates/                ← Plantillas HTML
│   ├── base.html                 ← Template base
│   ├── login.html
│   ├── registro.html
│   ├── index.html
│   ├── perfil.html
│   ├── rate_limit_error.html
│   └── ... (20+ templates)
│
├── static/                       ← Archivos estáticos
│   ├── css/                      ← Estilos
│   ├── js/                       ← Scripts
│   ├── img/                      ← Imágenes
│   ├── manifest.json             ← PWA manifest
│   └── sw.js                     ← Service Worker
│
├── 🗂️ DOCUMENTACIÓN
├── ├── docs/                     ⭐ NUEVO - Documentación
│   ├── ESTRUCTURA.md             ← Estructura del proyecto
│   ├── VALIDACION.md             ← Validadores
│   ├── RATE_LIMITING.md          ← Rate limiting
│   ├── API.md                    (futuro)
│   ├── DEPLOYMENT.md             (futuro)
│   └── CONTRIBUTING.md           (futuro)
│
├── 🗂️ CONFIGURACIÓN
├── ├── config/                   ⭐ NUEVO - Configuración
│   ├── logging.yaml              (futuro)
│   └── nginx.conf                (futuro)
│
├── 🗂️ DATOS
├── ├── instance/                 ← Archivos runtime (NO versionado)
│   └── finanzas.db               ← Base de datos
│
├── 📝 ENTRADA PRINCIPAL
├── ├── app.py                    ← LEGACY (compatible)
├── ├── app_new.py                ← NUEVO (recomendado)
│
├── 📋 ARCHIVOS DE CONFIGURACIÓN
├── ├── .env                      ← Variables de entorno (NO versionado)
├── ├── .env.example              ← Plantilla de .env
├── ├── .gitignore                ← Archivos a ignorar
├── ├── requirements.txt          ← Dependencias
├── ├── Procfile                  ← Heroku config
├── ├── pytest.ini                (futuro)
├── ├── setup.py                  (futuro)
├── └── docker-compose.yml        (futuro)
│
├── 📚 DOCUMENTACIÓN PRINCIPAL
├── ├── README.md                 ← Guía original
├── ├── README_NUEVO.md           ← Guía completa ⭐
├── ├── MIGRACION.md              ← Guía de migración ⭐
├── ├── REORGANIZACION_COMPLETADA.md  ← Resumen ⭐
├── ├── VALIDACION.md             ← Validadores
├── ├── RATE_LIMITING.md          ← Rate limiting
├── ├── IMPLEMENTACION_RATE_LIMITING.md
├── ├── CHANGELOG.md              (futuro)
├── ├── LICENSE                   ← MIT License
│
├── 📂 OTROS
├── ├── .git/                     ← Repositorio Git
├── ├── venv/                     ← Entorno virtual (NO versionado)
├── ├── __pycache__/              ← Caché Python (NO versionado)
├── ├── .pytest_cache/            ← Caché pytest (NO versionado)
│
└── 🗂️ GITHUB (futuro)
    ├── .github/
    │   ├── workflows/
    │   │   └── tests.yml         ← CI/CD con GitHub Actions
    │   └── ISSUE_TEMPLATE/
    │       ├── bug.md
    │       └── feature.md
    └── ...
```

## 📊 Distribución de archivos

### Por funcionalidad:
```
Autenticación:          routes/auth.py
Finanzas:               routes/finanzas.py
Validación:             src/validators.py
Seguridad:              src/rate_limiter.py
Base de datos:          src/models.py
Configuración:          src/config.py
Extensiones:            src/extensions.py
Tests:                  tests/
Interfaz:               templates/
Estilos:                static/css/
Scripts:                static/js/
```

### Por tipo de archivo:
```
Python (.py):           src/, routes/, tests/, app.py
HTML:                   templates/
CSS:                    static/css/
JavaScript:             static/js/
Configuración:          .env, config/, pytest.ini
Documentación (.md):    docs/, *.md
Data:                   instance/finanzas.db
```

### Por tamaño:
```
GRANDES (>2KB):
  - routes/finanzas.py
  - src/models.py
  - templates/index.html

MEDIANOS (1-2KB):
  - routes/auth.py
  - src/validators.py
  - src/config.py

PEQUEÑOS (<1KB):
  - src/__init__.py
  - src/extensions.py
  - app_new.py
```

## 🎯 Roles de cada directorio

| Directorio | Responsabilidad | Archivos |
|-----------|----------------|----------|
| `src/` | Lógica de negocio | 7+ `.py` |
| `routes/` | Controladores | 4+ `.py` |
| `tests/` | Pruebas | 2+ `.py` |
| `templates/` | Vistas HTML | 20+ `.html` |
| `static/` | Assets | CSS, JS, IMG |
| `docs/` | Documentación | `.md` |
| `config/` | Configuración | YAML, CONF |
| `instance/` | Runtime | `.db` |

## 📈 Flujo de datos

```
┌─────────────┐
│   Cliente   │ (Browser)
└──────┬──────┘
       │
       ▼
┌────────────────────────────────────┐
│  app.py / app_new.py              │ (Punto de entrada)
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  src/core.py (create_app)         │ (Factory)
└──────────┬─────────────────────────┘
           │
           ├─► src/config.py         (Configuración)
           ├─► src/extensions.py     (Extensiones)
           ├─► src/models.py         (Modelos)
           └─► routes/               (Blueprints)
               ├─► routes/auth.py
               ├─► routes/finanzas.py
               ├─► routes/usuario.py
               └─► routes/extras.py
                   │
                   ├─► src/validators.py
                   ├─► src/rate_limiter.py
                   └─► src/models.py
                       │
                       ▼
                    SQLite/PostgreSQL
```

## 🔀 Comparación: Antes vs Después

### ANTES (Estructura plana)
```
finanzas/
├── app.py
├── config.py
├── models.py
├── extensions.py
├── validators.py
├── rate_limiter.py
├── tests_validators.py
├── tests_rate_limiter.py
├── README.md
├── VALIDACION.md
├── RATE_LIMITING.md
└── routes/
```
**Problemas:** Caótico, difícil de navegar, no escala.

### DESPUÉS (Estructura jerárquica)
```
finanzas/
├── src/                 ← Código
│   ├── core.py
│   ├── config.py
│   └── ...
├── routes/              ← Controladores
├── tests/               ← Pruebas
├── docs/                ← Documentación
├── config/              ← Configuración
├── templates/
├── static/
└── app.py / app_new.py
```
**Ventajas:** Claro, escalable, profesional.

## 🎓 Convenciones

### Archivos
- `*.py` - Python
- `*.html` - Templates
- `*.css` - Estilos
- `*.js` - Scripts
- `*.md` - Documentación
- `*.yml/.yaml` - Configuración
- `*.db` - Base de datos

### Directorios
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation
- `config/` - Configuration
- `routes/` - Flask blueprints
- `templates/` - HTML templates
- `static/` - Assets

### Nombres
- `core.py` - Main application
- `config.py` - Configuration
- `models.py` - Database models
- `validators.py` - Input validation
- `test_*.py` - Test files
- `__init__.py` - Package marker

## ✅ Checklist de uso

- [ ] Crear el proyecto con esta estructura
- [ ] Ejecutar con `python app_new.py`
- [ ] Tests pasen con `pytest tests/`
- [ ] Documentar cambios en `docs/`
- [ ] Mantener estructura consistente
- [ ] Agregar archivos en lugares correctos
- [ ] Actualizar imports relativos

---

**Última actualización**: 28 de abril de 2026
**Estado**: ✅ Estructura completa y funcional
