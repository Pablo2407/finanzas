# 🗂️ ÍNDICE RÁPIDO - Encuentra lo que necesitas

## 🎯 ¿Qué necesitas?

### 🆕 Nuevo en el proyecto?
**Empieza aquí:**
1. [QUICKSTART.md](QUICKSTART.md) ← 30 segundos
2. [GETTING_STARTED.md](GETTING_STARTED.md) ← 5 minutos
3. [README_NUEVO.md](README_NUEVO.md) ← 10 minutos
4. [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md) ← 5 minutos

### ⚙️ ¿Cómo ejecuto la app?
- Ver: [QUICKSTART.md](QUICKSTART.md#30-segundos-para-empezar)
- Comando: `python app_new.py`
- URL: http://localhost:5000

### 🧪 ¿Cómo ejecuto tests?
- Ver: [QUICKSTART.md](QUICKSTART.md#ejecutar-tests)
- Comando: `pytest tests/ -v`
- Esperado: 24/24 tests ✅

### 📖 ¿Cómo entiendo la estructura?
- Ver: [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md)
- O: [docs/VISUALIZACION.md](docs/VISUALIZACION.md)
- O: Mira el diagrama en [TABLA_CONTENIDOS.md](TABLA_CONTENIDOS.md)

### 🔧 ¿Cómo agrego una nueva feature?
1. Lee: [MIGRACION.md](MIGRACION.md) - Para entender imports
2. Crea archivo en `routes/` o `src/`
3. Importa correctamente desde `src/`
4. Ejecuta tests: `pytest tests/ -v`

### 🛡️ ¿Cómo valido datos?
- Ver: [VALIDACION.md](VALIDACION.md)
- Usar: `from src.validators import validar_email, validar_contraseña`
- Ejemplo: `validar_email("test@example.com")`

### 🔐 ¿Cómo funciona rate limiting?
- Ver: [RATE_LIMITING.md](RATE_LIMITING.md)
- Protegidos: login, registro, recuperar, 2FA, restablecer
- Límites: 3-10 requests por minuto

### 💾 ¿Cómo accedo a la base de datos?
- Ver: [src/models.py](src/models.py)
- Usar: `from src.models import Usuario, Transaccion`
- Guardar: `db.session.add(obj); db.session.commit()`

### 🚀 ¿Cómo despliego a producción?
- Ver: [README_NUEVO.md](README_NUEVO.md#despliegue)
- Variables: Configurar `.env` para producción
- Comando: `python app_new.py` (o usar gunicorn)

### ❓ Tengo un error
- Ver: [QUICKSTART.md](QUICKSTART.md#troubleshooting)
- Busca tu error en la tabla
- Sigue las soluciones

---

## 📚 Índice por tipo de documento

### 📖 GUÍAS PRINCIPALES
| Documento | Duración | Para... | Urgencia |
|-----------|----------|---------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5 min | Empezar rápido | ⭐⭐⭐⭐⭐ |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 10 min | Instalación completa | ⭐⭐⭐⭐⭐ |
| [README_NUEVO.md](README_NUEVO.md) | 15 min | Entender todo | ⭐⭐⭐⭐ |
| [TABLA_CONTENIDOS.md](TABLA_CONTENIDOS.md) | 5 min | Navegar docs | ⭐⭐⭐ |

### 🏗️ ARQUITECTURA
| Documento | Tipo | Para... | Lee si... |
|-----------|------|---------|-----------|
| [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md) | Visualización | Ver carpetas | Quieres entender organización |
| [docs/VISUALIZACION.md](docs/VISUALIZACION.md) | Diagrama | Ver flujos | Quieres ver flujo de datos |
| [MIGRACION.md](MIGRACION.md) | Técnico | Migrar código | Cambió la estructura |

### 🔧 TÉCNICO
| Documento | Tema | Para... |
|-----------|------|---------|
| [VALIDACION.md](VALIDACION.md) | Validadores | Validar datos |
| [RATE_LIMITING.md](RATE_LIMITING.md) | Rate limiting | Limitar requests |
| [IMPLEMENTACION_RATE_LIMITING.md](IMPLEMENTACION_RATE_LIMITING.md) | Implementación | Detalles técnicos |

### 📊 RESUMEN
| Documento | Contenido | Útil para... |
|-----------|-----------|--------------|
| [REORGANIZACION_COMPLETADA.md](REORGANIZACION_COMPLETADA.md) | Lo que se hizo | Ver cambios realizados |

---

## 🎯 Caminos típicos

### "Acabo de descargar el proyecto"
```
QUICKSTART.md
    ↓
python app_new.py
    ↓
http://localhost:5000
    ↓
¡Funciona! ✅
```

### "Quiero entenderlo todo"
```
GETTING_STARTED.md (checklist)
    ↓
README_NUEVO.md (guía completa)
    ↓
docs/ESTRUCTURA.md (arquitectura)
    ↓
Explora src/ y routes/
    ↓
¡Lo entiendo! 🎓
```

### "Tengo un error"
```
QUICKSTART.md → Troubleshooting
    ↓
¿Lo encontraste?
    ├─ Sí → Sigue la solución
    └─ No → Busca en README_NUEVO.md
    ↓
¿Problema resuelto?
```

### "Quiero agregar una feature"
```
MIGRACION.md (para imports)
    ↓
ESTRUCTURA.md (donde va)
    ↓
Crea el archivo
    ↓
Imports correctos
    ↓
pytest tests/ (verifica)
    ↓
¡Hecho! 🚀
```

### "Quiero validar datos"
```
VALIDACION.md (documentación)
    ↓
from src.validators import ...
    ↓
Usa validar_email(), validar_contraseña(), etc.
    ↓
Maneja respuesta (bool, mensaje)
```

### "Quiero limitar requests"
```
RATE_LIMITING.md (documentación)
    ↓
Usa @limiter.limit() en rutas
    ↓
Configura límites en src/rate_limiter.py
    ↓
Tests con pytest
```

---

## 📂 Estructura de archivos

```
finanzas/
│
├── 📖 DOCUMENTACIÓN (empieza aquí)
│   ├── QUICKSTART.md                    ⭐ EMPIZA AQUÍ
│   ├── GETTING_STARTED.md               ⭐ CHECKLIST
│   ├── INDICE.md                        ← Tú estás aquí
│   ├── TABLA_CONTENIDOS.md              ← Tabla completa
│   ├── README_NUEVO.md                  ← Guía principal
│   ├── MIGRACION.md                     ← Cambios
│   ├── REORGANIZACION_COMPLETADA.md     ← Resumen
│   ├── VALIDACION.md                    ← Validadores
│   ├── RATE_LIMITING.md                 ← Rate limiting
│   ├── IMPLEMENTACION_RATE_LIMITING.md
│   └── docs/
│       ├── ESTRUCTURA.md                ← Visualización
│       └── VISUALIZACION.md             ← Diagramas
│
├── 💻 CÓDIGO
│   ├── src/                             ← Lógica
│   ├── routes/                          ← Rutas
│   ├── templates/                       ← HTML
│   ├── static/                          ← CSS/JS
│   └── app_new.py                       ← Ejecuta esto
│
├── 🧪 TESTS
│   └── tests/
│       ├── test_validators.py           (17 tests ✅)
│       └── test_rate_limiter.py         (7 tests ✅)
│
└── ⚙️ CONFIGURACIÓN
    ├── .env                             ← Variables secretas
    └── requirements.txt                 ← Dependencias
```

---

## 🔍 Buscar por palabra clave

### Autenticación / Login
- Archivo: [routes/auth.py](routes/auth.py)
- Doc: [README_NUEVO.md](README_NUEVO.md#autenticación)
- Tests: [tests/test_*.py](tests/)

### Base de datos / SQL
- Archivo: [src/models.py](src/models.py)
- Config: [src/config.py](src/config.py)
- Doc: [README_NUEVO.md](README_NUEVO.md#base-de-datos)

### Validación
- Archivo: [src/validators.py](src/validators.py)
- Doc: [VALIDACION.md](VALIDACION.md)
- Tests: [tests/test_validators.py](tests/test_validators.py)

### Seguridad
- Rate limit: [src/rate_limiter.py](src/rate_limiter.py)
- 2FA: [routes/auth.py](routes/auth.py)
- Doc: [RATE_LIMITING.md](RATE_LIMITING.md)

### Configuración
- Archivo: [src/config.py](src/config.py)
- Variables: [.env](.env.example)
- Doc: [README_NUEVO.md](README_NUEVO.md#configuración)

### Rutas / URLs
- Archivos: [routes/](routes/)
- Lista: [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md)
- Doc: [README_NUEVO.md](README_NUEVO.md#endpoints)

### Tests
- Validators: [tests/test_validators.py](tests/test_validators.py)
- Rate limit: [tests/test_rate_limiter.py](tests/test_rate_limiter.py)
- Ejecutar: [QUICKSTART.md](QUICKSTART.md#ejecutar-tests)

### Despliegue
- Doc: [README_NUEVO.md](README_NUEVO.md#despliegue)
- Config: [src/config.py](src/config.py)
- Dockerfile: (próximamente)

### Solución de problemas
- Doc: [QUICKSTART.md](QUICKSTART.md#troubleshooting)
- Checklist: [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting)

---

## ⭐ Archivos más importantes

1. **[QUICKSTART.md](QUICKSTART.md)** - Comienza aquí
2. **[app_new.py](app_new.py)** - Ejecuta esto
3. **[README_NUEVO.md](README_NUEVO.md)** - Lee después
4. **[src/models.py](src/models.py)** - Modelos de BD
5. **[routes/auth.py](routes/auth.py)** - Autenticación
6. **[src/validators.py](src/validators.py)** - Validación

---

## 📊 Estadísticas

- **Archivos de documentación**: 12+
- **Archivos Python**: 15+
- **Líneas de código**: ~3000+
- **Líneas de documentación**: ~2000+
- **Tests**: 24 ✅
- **Endpoints protegidos**: 5
- **Validadores**: 5
- **Modelos de BD**: 6

---

## 🎓 Aprende

### Nivel 1: Beginner
1. Lee: QUICKSTART.md
2. Ejecuta: `python app_new.py`
3. Accede: http://localhost:5000

### Nivel 2: Intermediate
1. Lee: README_NUEVO.md
2. Explora: [src/](src/) y [routes/](routes/)
3. Ejecuta: `pytest tests/ -v`

### Nivel 3: Advanced
1. Lee: MIGRACION.md
2. Lee: docs/VISUALIZACION.md
3. Modifica: models.py, validators.py
4. Crea: nuevas rutas

### Nivel 4: Expert
1. Lee: IMPLEMENTACION_RATE_LIMITING.md
2. Agrega: nuevas features
3. Deploy: a producción
4. Monitor: en producción

---

## ✅ Checklist de lectura

- [ ] QUICKSTART.md (5 min)
- [ ] GETTING_STARTED.md (10 min)
- [ ] README_NUEVO.md (15 min)
- [ ] docs/ESTRUCTURA.md (5 min)
- [ ] TABLA_CONTENIDOS.md (3 min)

**Total**: ~40 minutos para entender todo ✅

---

## 🆘 Ayuda rápida

| Pregunta | Respuesta |
|----------|-----------|
| ¿Cómo empiezo? | Lee QUICKSTART.md |
| ¿Cómo instalo? | Lee GETTING_STARTED.md |
| ¿Cómo ejecuto? | `python app_new.py` |
| ¿Cómo test? | `pytest tests/ -v` |
| ¿Dónde está X? | Busca en TABLA_CONTENIDOS.md |
| Tengo error | Ve a QUICKSTART.md → Troubleshooting |
| Quiero entender | Lee README_NUEVO.md |
| Quiero agregar feature | Ve a MIGRACION.md |
| Quiero validar | Lee VALIDACION.md |
| Quiero limitar | Lee RATE_LIMITING.md |

---

**Última actualización**: 28 de abril de 2026

**Tiempo estimado**: 2 minutos para leer este documento

**Siguiente paso**: Elige tu camino arriba 👆
