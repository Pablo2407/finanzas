# 📋 Getting Started Checklist

## ✅ Pre-requisitos verificados

- [x] Python 3.8+
- [x] pip
- [x] git
- [x] SQLite (incluido en Python)
- [x] Navegador moderno
- [x] Terminal/CMD

## 🚀 Instalación (5 minutos)

### Paso 1: Descargar el proyecto
```bash
[ ] git clone <tu-repo> finanzas
[ ] cd finanzas
```

### Paso 2: Crear entorno virtual
```bash
[ ] python3 -m venv venv
[ ] source venv/bin/activate  # En Windows: venv\Scripts\activate
[ ] Verificar: which python3  # Debe mostrar ruta con venv
```

### Paso 3: Instalar dependencias
```bash
[ ] pip install -r requirements.txt
[ ] pip show flask              # Verificar Flask 3.1.3
```

### Paso 4: Configurar variables
```bash
[ ] cp .env.example .env
[ ] nano .env                   # Editar con tus valores
[ ] Verificar FLASK_ENV=development
```

### Paso 5: Inicializar base de datos
```bash
[ ] python -c "from src.core import app, db; app.app_context().push(); db.create_all()"
[ ] Verificar: ls -la instance/finanzas.db
```

### Paso 6: Ejecutar la app
```bash
[ ] python app_new.py
[ ] Abrir: http://localhost:5000
[ ] ¡Ver home page!
```

## 🧪 Testing (2 minutos)

```bash
[ ] pytest tests/ -v
[ ] Resultado esperado: 24 passed
[ ] Tiempo: ~2-5 segundos
```

## 📁 Verificar estructura

```bash
[ ] ls -la src/        # 7 archivos .py
[ ] ls -la routes/     # 4 archivos .py
[ ] ls -la tests/      # 2 archivos .py
[ ] ls -la templates/  # 20+ archivos .html
[ ] ls -la static/     # CSS, JS, IMG
```

## 🔐 Verificar funcionalidades

### Registro
```bash
[ ] Ir a http://localhost:5000/registro
[ ] Intentar email inválido → Error
[ ] Intentar contraseña débil → Error
[ ] Registrar usuario válido → Éxito
```

### Login
```bash
[ ] Ir a http://localhost:5000/login
[ ] Intentar login 5+ veces → Rate limit error (429)
[ ] Esperar 1 minuto
[ ] Login exitoso
```

### Validadores
```bash
[ ] pytest tests/test_validators.py -v
[ ] Debe pasar: 17 tests
```

### Rate Limiting
```bash
[ ] pytest tests/test_rate_limiter.py -v
[ ] Debe pasar: 7 tests
```

## 📚 Leer documentación

```bash
[ ] QUICKSTART.md (5 min)                    ← Empieza aquí
[ ] README_NUEVO.md (10 min)                 ← Guía completa
[ ] docs/ESTRUCTURA.md (5 min)               ← Visualización
[ ] TABLA_CONTENIDOS.md (3 min)              ← Índice
```

## 🛠️ Desarrollo (después de instalar)

### Crear nueva ruta
```bash
[ ] Crear archivo en routes/nueva.py
[ ] Importar en src/core.py
[ ] Registrar blueprint: app.register_blueprint(...)
[ ] Reiniciar: python app_new.py
```

### Crear nuevo modelo
```bash
[ ] Definir en src/models.py
[ ] Ejecutar: python -c "from src.core import db; db.create_all()"
[ ] Verificar en instance/finanzas.db
```

### Agregar test
```bash
[ ] Crear en tests/test_*.py
[ ] Ejecutar: pytest tests/test_*.py -v
[ ] Todos deben pasar
```

## 🔍 Troubleshooting

### Problema: "Module not found"
```bash
[ ] Verificar que venv está activado: which python
[ ] Reinstalar: pip install -r requirements.txt --force-reinstall
[ ] Limpiar caché: find . -type d -name __pycache__ -exec rm -r {} +
```

### Problema: "Port 5000 already in use"
```bash
[ ] Cambiar puerto: python -c "from src.core import app; app.run(port=5001)"
[ ] O matar proceso: lsof -i :5000 | kill -9 <PID>
```

### Problema: "Database locked"
```bash
[ ] Detener app
[ ] Eliminar .db: rm instance/finanzas.db
[ ] Reinicializar: python -c "from src.core import app, db; app.app_context().push(); db.create_all()"
```

### Problema: Tests fallan
```bash
[ ] Limpiar pytest cache: rm -rf .pytest_cache
[ ] Limpiar Python cache: find . -name "*.pyc" -delete
[ ] Ejecutar nuevamente: pytest tests/ -v
```

## 📊 Verificación final

### Estructura de código
```bash
[ ] wc -l src/*.py                          # ~3000 líneas
[ ] wc -l routes/*.py                       # ~1000 líneas
[ ] wc -l tests/*.py                        # ~500 líneas
```

### Documentación
```bash
[ ] ls -1 *.md | wc -l                      # ~8 archivos
[ ] wc -l *.md                              # ~1930 líneas
[ ] cat docs/ESTRUCTURA.md | wc -l          # ~300 líneas
```

### Tests
```bash
[ ] pytest tests/ -v                        # 24/24 PASSED
[ ] pytest tests/ --cov=src --cov=routes   # >85% coverage
```

### Seguridad
```bash
[ ] python -c "from src.validators import validar_contraseña; print(validar_contraseña('Test123!'))"
[ ] Resultado: (True, '')
[ ] python -c "from src.validators import validar_contraseña; print(validar_contraseña('test'))"
[ ] Resultado: (False, 'error message')
```

## 🎯 Milestones

### Semana 1: Familiarización
- [ ] Instalar proyecto
- [ ] Leer README_NUEVO.md
- [ ] Ejecutar app
- [ ] Ejecutar tests
- [ ] Explorar código

### Semana 2: Desarrollo
- [ ] Crear primera rama (git branch)
- [ ] Hacer cambios pequeños
- [ ] Ejecutar tests
- [ ] Hacer commit
- [ ] Hacer PR

### Semana 3: Profundización
- [ ] Entender arquitectura
- [ ] Modificar modelos
- [ ] Agregar validadores
- [ ] Crear rutas nuevas

### Semana 4: Producción
- [ ] Configurar .env para producción
- [ ] Crear Dockerfile (opcional)
- [ ] Configurar CI/CD
- [ ] Desplegar

## 🌟 Tips y trucos

```bash
# Ver estructura en árbol
tree -L 2 -I 'venv|__pycache__'

# Ejecutar con debug
FLASK_DEBUG=1 python app_new.py

# Ver logs
tail -f logs/app.log

# Ejecutar tests con cobertura
pytest --cov=src --cov=routes tests/

# Contar líneas de código
find src routes -name "*.py" -exec wc -l {} +

# Generar requerimientos actualizado
pip freeze > requirements.txt

# Limpiar todo
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf .pytest_cache 2>/dev/null

# Entrar en shell de Python
python -c "from src.core import app; app.app_context().push()"

# Ver endpoints disponibles
python -c "from src.core import app; print([f'{rule.rule} [{rule.methods}]' for rule in app.url_map.iter_rules()])"
```

## 📞 Contacto y ayuda

- **Documentación**: [TABLA_CONTENIDOS.md](TABLA_CONTENIDOS.md)
- **Preguntas frecuentes**: [QUICKSTART.md](QUICKSTART.md) - Troubleshooting
- **Problema específico**: Busca en [README_NUEVO.md](README_NUEVO.md)
- **Error técnico**: Consulta [VALIDACION.md](VALIDACION.md) o [RATE_LIMITING.md](RATE_LIMITING.md)

## ✨ Siguientes pasos después de Getting Started

1. **Personalizacionr**: Cambiar logo, colores, nombre
2. **Agregar features**: Nuevas funcionalidades
3. **Mejorar seguridad**: HTTPS, CAPTCHA, etc.
4. **Optimizar BD**: Índices, queries
5. **Monitoreo**: Logs, alertas
6. **Despliegue**: Producción
7. **Mantenimiento**: Updates, patches

## 🎉 ¡Listo!

Si completaste todos los checkboxes, ¡tu proyecto está listo para desarrollo!

**Próximo paso**: Abre [QUICKSTART.md](QUICKSTART.md) o [README_NUEVO.md](README_NUEVO.md)

---

*Última actualización: 28 de abril de 2026*

**Tiempo estimado**: 5-10 minutos

**Dificultad**: 🟢 Fácil

**Requisitos**: Python 3.8+, pip, git
