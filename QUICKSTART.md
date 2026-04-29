# 🚀 Quick Start - Guía Rápida

## ⚡ 30 segundos para empezar

```bash
# 1. Clonar y entrar
cd /home/pablo/finanzas
source venv/bin/activate

# 2. Ejecutar la app
python app_new.py

# 3. Acceder en navegador
# http://localhost:5000
```

¡Listo! 🎉

---

## 📋 Guía completa (2 minutos)

### 1️⃣ Clonar el repositorio
```bash
git clone <tu-repo>
cd finanzas
```

### 2️⃣ Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tus valores
nano .env
```

Variables necesarias:
```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///instance/finanzas.db
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-app
```

### 5️⃣ Inicializar base de datos
```bash
python -c "from src.core import app, db; app.app_context().push(); db.create_all()"
```

### 6️⃣ Ejecutar la app
```bash
# Opción 1: Legacy (sigue funcionando)
python app.py

# Opción 2: Nueva estructura (recomendado)
python app_new.py

# Opción 3: Directamente
python -c "from src.core import app; app.run(debug=True)"
```

### 7️⃣ Acceder en navegador
```
http://localhost:5000
```

---

## 🧪 Ejecutar tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_validators.py -v
pytest tests/test_rate_limiter.py -v

# Con cobertura
pytest tests/ --cov=src --cov=routes
```

**Resultado esperado:** 24/24 tests ✅

---

## 📁 Estructura rápida

```
src/               ← Código fuente
├── core.py        ← Factory de app
├── config.py      ← Configuración
├── models.py      ← BD
├── validators.py  ← Validadores
├── extensions.py  ← Extensiones

routes/            ← Controladores
├── auth.py        ← Login/Registro
├── finanzas.py    ← Transacciones

tests/             ← Pruebas
├── test_validators.py
└── test_rate_limiter.py

templates/         ← HTML
static/            ← CSS/JS
docs/              ← Documentación
```

---

## 🔑 Archivos principales

| Archivo | Propósito |
|---------|-----------|
| `app.py` | Entry point legacy |
| `app_new.py` | Entry point nuevo |
| `src/core.py` | Factory Flask |
| `src/config.py` | Config por entorno |
| `.env` | Variables secretas |
| `requirements.txt` | Dependencias |

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Asegúrate de estar en el venv
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Port 5000 in use"
```bash
# Cambia el puerto
python -c "from src.core import app; app.run(port=5001)"
```

### Error: "Database not found"
```bash
# Reinicia la BD
python -c "from src.core import app, db; app.app_context().push(); db.create_all()"
```

### Tests fallan
```bash
# Limpia caché
rm -rf .pytest_cache __pycache__
pytest tests/ -v
```

---

## 🚀 Comandos útiles

```bash
# Ver estructura
tree -L 2 -I 'venv|__pycache__'

# Ver logs
tail -f logs/app.log

# Generar requerimientos
pip freeze > requirements.txt

# Limpiar caché
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Tests con cobertura
pytest --cov=src --cov=routes tests/

# Ejecutar servidor de producción
gunicorn "src.core:app"
```

---

## 📚 Documentación completa

- **README_NUEVO.md** - Guía principal
- **MIGRACION.md** - Guía de migración
- **REORGANIZACION_COMPLETADA.md** - Resumen
- **docs/ESTRUCTURA.md** - Estructura visual
- **docs/VALIDACION.md** - Validadores
- **docs/RATE_LIMITING.md** - Rate limiting

---

## ❓ Preguntas frecuentes

**P: ¿Cuál debo usar, app.py o app_new.py?**
R: Usa `app_new.py` (nueva estructura). `app.py` es legacy.

**P: ¿Cómo agrego una nueva ruta?**
R: Crea en `routes/nuevo.py` y registra en `src/core.py`.

**P: ¿Dónde pongo los tests?**
R: En `tests/test_*.py`. Sigue el patrón de los existentes.

**P: ¿Cómo cambio de BD?**
R: Actualiza `DATABASE_URL` en `.env` y `src/config.py`.

**P: ¿Cómo despliego a producción?**
R: Lee `DEPLOYMENT.md` (próximamente en docs/).

---

## ✨ Próximos pasos

1. **Configurar .env** - Variables de entorno
2. **Instalar dependencias** - `pip install -r requirements.txt`
3. **Ejecutar tests** - `pytest tests/ -v`
4. **Iniciar app** - `python app_new.py`
5. **Acceder** - http://localhost:5000

---

¿Necesitas ayuda? Consulta los archivos `.md` en `docs/` o `MIGRACION.md`.

**Estado:** ✅ Proyecto listo para desarrollo

---

*Última actualización: 28 de abril de 2026*
