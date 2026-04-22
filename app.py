from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Transaccion, Presupuesto, Categoria, Recurrente, Meta
from itsdangerous import URLSafeTimedSerializer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


from flask_mail import Mail, Message

from flask import send_file
import openpyxl
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_123'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'martinezmestrajuanpablo7@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxpf lxqu slti jidv'

mail = Mail(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'landing'

@app.context_processor
def inject_moneda():
    if current_user and current_user.is_authenticated:
        return dict(moneda=current_user.moneda)
    return dict(moneda='$')



@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if len(username) < 3:
            flash('El usuario debe tener al menos 3 caracteres')
            return redirect(url_for('registro'))

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado')
            return redirect(url_for('registro'))

        nuevo = Usuario(username=username, email=email, password=generate_password_hash(password))
        db.session.add(nuevo)
        db.session.commit()

        try:
            msg = Message('Bienvenido a Mis Finanzas',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email])
            msg.body = f'Hola {username}, tu cuenta fue creada exitosamente. ¡Bienvenido!'
            mail.send(msg)
        except:
            pass

        flash('Cuenta creada exitosamente, inicia sesión')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(username=request.form['username']).first()
        if usuario and check_password_hash(usuario.password, request.form['password']):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    from datetime import datetime
    categoria_filtro = request.args.get('categoria', '')
    fecha_filtro = request.args.get('fecha', '')

    query = Transaccion.query.filter_by(usuario_id=current_user.id)

    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)

    if fecha_filtro:
        fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d')
        query = query.filter(db.func.date(Transaccion.fecha) == fecha.date())

    transacciones = query.order_by(Transaccion.fecha.desc()).all()
    todas = Transaccion.query.filter_by(usuario_id=current_user.id).all()

    # Balance general
    ingresos_total = sum(t.monto for t in todas if t.tipo == 'ingreso')
    gastos_total = sum(t.monto for t in todas if t.tipo == 'gasto')
    balance = ingresos_total - gastos_total

    # Stats del mes actual
    mes_actual = datetime.now().strftime('%Y-%m')
    transacciones_mes = [t for t in todas if t.fecha.strftime('%Y-%m') == mes_actual]
    ingresos_mes = sum(t.monto for t in transacciones_mes if t.tipo == 'ingreso')
    gastos_mes = sum(t.monto for t in transacciones_mes if t.tipo == 'gasto')
    num_transacciones = len(transacciones_mes)
    mayor_gasto = max((t.monto for t in transacciones_mes if t.tipo == 'gasto'), default=0)

    categorias_base = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    categorias_personalizadas = Categoria.query.filter_by(usuario_id=current_user.id).all()
    categorias_lista = categorias_base + [c.nombre for c in categorias_personalizadas]
    montos_lista = [sum(t.monto for t in todas if t.tipo == 'gasto' and t.categoria == cat) for cat in categorias_lista]

    return render_template('index.html',
        transacciones=transacciones,
        balance=round(balance, 2),
        categorias=categorias_lista,
        montos=montos_lista,
        filtro=categoria_filtro,
        fecha_filtro=fecha_filtro,
        categorias_personalizadas=categorias_personalizadas,
        ingresos_mes=round(ingresos_mes, 2),
        gastos_mes=round(gastos_mes, 2),
        num_transacciones=num_transacciones,
        mayor_gasto=round(mayor_gasto, 2)
    )
    categoria_filtro = request.args.get('categoria', '')
    fecha_filtro = request.args.get('fecha', '')

    query = Transaccion.query.filter_by(usuario_id=current_user.id)

    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)

    if fecha_filtro:
        from datetime import datetime
        fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d')
        query = query.filter(db.func.date(Transaccion.fecha) == fecha.date())

    transacciones = query.order_by(Transaccion.fecha.desc()).all()

    ingresos = sum(t.monto for t in transacciones if t.tipo == 'ingreso')
    gastos = sum(t.monto for t in transacciones if t.tipo == 'gasto')
    balance = ingresos - gastos

    categorias_base = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    categorias_personalizadas = Categoria.query.filter_by(usuario_id=current_user.id).all()
    categorias_lista = categorias_base + [c.nombre for c in categorias_personalizadas]
    montos_lista = [sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.categoria == cat) for cat in categorias_lista]

    return render_template('index.html',
        transacciones=transacciones,
        balance=round(balance, 2),
        categorias=categorias_lista,
        montos=montos_lista,
        filtro=categoria_filtro,
        fecha_filtro=fecha_filtro,
        categorias_personalizadas=categorias_personalizadas
    )

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    from datetime import datetime
    nueva = Transaccion(
        descripcion=request.form['descripcion'],
        monto=float(request.form['monto']),
        tipo=request.form['tipo'],
        categoria=request.form['categoria'],
        usuario_id=current_user.id
    )
    db.session.add(nueva)
    db.session.commit()

    # Verificar presupuesto
    if nueva.tipo == 'gasto':
        mes_actual = datetime.now().strftime('%Y-%m')
        presupuesto = Presupuesto.query.filter_by(
            usuario_id=current_user.id,
            categoria=nueva.categoria,
            mes=mes_actual
        ).first()

        if presupuesto and presupuesto.monto > 0:
            transacciones = Transaccion.query.filter_by(
                usuario_id=current_user.id,
                categoria=nueva.categoria
            ).all()
            gastado = sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.fecha.strftime('%Y-%m') == mes_actual)
            porcentaje = (gastado / presupuesto.monto) * 100

            if porcentaje >= 80:
                try:
                    msg = Message('⚠️ Alerta de presupuesto',
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[current_user.email])
                    msg.body = f'''Hola {current_user.username},

Has usado el {round(porcentaje)}% de tu presupuesto de {nueva.categoria}.

Presupuesto: ${presupuesto.monto}
Gastado: ${round(gastado, 2)}
Disponible: ${round(presupuesto.monto - gastado, 2)}

¡Ten cuidado con tus gastos!

- Mis Finanzas'''
                    mail.send(msg)
                except:
                    pass

    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    transaccion = Transaccion.query.get_or_404(id)
    if transaccion.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar esta transacción')
        return redirect(url_for('index'))
    db.session.delete(transaccion)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    transaccion = Transaccion.query.get_or_404(id)
    if transaccion.usuario_id != current_user.id:
        flash('No tienes permiso para editar esta transacción')
        return redirect(url_for('index'))
    if request.method == 'POST':
        transaccion.descripcion = request.form['descripcion']
        transaccion.monto = float(request.form['monto'])
        transaccion.tipo = request.form['tipo']
        transaccion.categoria = request.form['categoria']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', transaccion=transaccion)

@app.route('/resumen')
@login_required
def resumen():
    from datetime import datetime
    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).all()

    resumen_meses = {}
    for t in transacciones:
        mes = t.fecha.strftime('%Y-%m')
        if mes not in resumen_meses:
            resumen_meses[mes] = {'ingresos': 0, 'gastos': 0}
        if t.tipo == 'ingreso':
            resumen_meses[mes]['ingresos'] += t.monto
        else:
            resumen_meses[mes]['gastos'] += t.monto

    return render_template('resumen.html', resumen=resumen_meses)

@app.route('/exportar')
@login_required
def exportar():
    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Finanzas'

    ws.append(['Descripcion', 'Monto', 'Tipo', 'Categoria', 'Fecha'])

    for t in transacciones:
        ws.append([t.descripcion, t.monto, t.tipo, t.categoria, t.fecha.strftime('%d/%m/%Y')])

    archivo = io.BytesIO()
    wb.save(archivo)
    archivo.seek(0)

    return send_file(archivo, download_name='finanzas.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/perfil/username', methods=['POST'])
@login_required
def cambiar_username():
    username = request.form['username'].strip()

    if len(username) < 3:
        flash('El usuario debe tener al menos 3 caracteres', 'username')
        return redirect(url_for('perfil'))

    if Usuario.query.filter_by(username=username).first():
        flash('Ese usuario ya existe', 'username')
        return redirect(url_for('perfil'))

    current_user.username = username
    db.session.commit()
    flash('Usuario actualizado exitosamente', 'username')
    return redirect(url_for('perfil'))

@app.route('/perfil/password', methods=['POST'])
@login_required
def cambiar_password():
    password_actual = request.form['password_actual']
    password_nuevo = request.form['password_nuevo']
    password_confirmar = request.form['password_confirmar']

    if not check_password_hash(current_user.password, password_actual):
        flash('La contraseña actual es incorrecta', 'password')
        return redirect(url_for('perfil'))

    if len(password_nuevo) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres', 'password')
        return redirect(url_for('perfil'))

    if password_nuevo != password_confirmar:
        flash('Las contraseñas no coinciden', 'password')
        return redirect(url_for('perfil'))

    current_user.password = generate_password_hash(password_nuevo)
    db.session.commit()
    flash('Contraseña actualizada exitosamente', 'password')
    return redirect(url_for('perfil'))

@app.route('/presupuesto')
@login_required
def presupuesto():
    from datetime import datetime
    mes_actual = datetime.now().strftime('%Y-%m')
    presupuestos = Presupuesto.query.filter_by(usuario_id=current_user.id, mes=mes_actual).all()
    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).all()

    datos = []
    categorias = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    for cat in categorias:
        gastado = sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.categoria == cat and t.fecha.strftime('%Y-%m') == mes_actual)
        presupuesto_cat = next((p.monto for p in presupuestos if p.categoria == cat), 0)
        porcentaje = (gastado / presupuesto_cat * 100) if presupuesto_cat > 0 else 0
        datos.append({
            'categoria': cat,
            'presupuesto': presupuesto_cat,
            'gastado': round(gastado, 2),
            'porcentaje': min(round(porcentaje), 100),
            'excedido': gastado > presupuesto_cat and presupuesto_cat > 0
        })

    return render_template('presupuesto.html', datos=datos, mes=mes_actual)

@app.route('/presupuesto/guardar', methods=['POST'])
@login_required
def guardar_presupuesto():
    from datetime import datetime
    mes_actual = datetime.now().strftime('%Y-%m')
    categorias_base = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    categorias_personalizadas = Categoria.query.filter_by(usuario_id=current_user.id).all()
    categorias_lista = categorias_base + [c.nombre for c in categorias_personalizadas]

    for cat in categorias:
        monto = request.form.get(cat, 0)
        if monto:
            existente = Presupuesto.query.filter_by(usuario_id=current_user.id, categoria=cat, mes=mes_actual).first()
            if existente:
                existente.monto = float(monto)
            else:
                nuevo = Presupuesto(categoria=cat, monto=float(monto), mes=mes_actual, usuario_id=current_user.id)
                db.session.add(nuevo)

    db.session.commit()
    return redirect(url_for('presupuesto'))

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email'].strip()
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            token = serializer.dumps(email, salt='recuperar-password')
            enlace = url_for('restablecer', token=token, _external=True)
            try:
                msg = Message('Recuperar contraseña',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email])
                msg.body = f'Hola {usuario.username}, haz clic en este enlace para restablecer tu contraseña:\n\n{enlace}\n\nEste enlace expira en 30 minutos.'
                mail.send(msg)
            except:
                pass
        flash('Si el correo existe recibirás un enlace para restablecer tu contraseña')
        return redirect(url_for('login'))
    return render_template('recuperar.html')

@app.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer(token):
    try:
        email = serializer.loads(token, salt='recuperar-password', max_age=1800)
    except:
        flash('El enlace ha expirado o no es válido')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        confirmar = request.form['confirmar']

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres')
            return redirect(url_for('restablecer', token=token))

        if password != confirmar:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('restablecer', token=token))

        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = generate_password_hash(password)
        db.session.commit()
        flash('Contraseña restablecida exitosamente')
        return redirect(url_for('login'))

    return render_template('restablecer.html', token=token)

@app.route('/graficas')
@login_required
def graficas():
    from datetime import datetime
    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).order_by(Transaccion.fecha).all()

    # Ingresos y gastos por mes
    datos_meses = {}
    for t in transacciones:
        mes = t.fecha.strftime('%Y-%m')
        if mes not in datos_meses:
            datos_meses[mes] = {'ingresos': 0, 'gastos': 0}
        if t.tipo == 'ingreso':
            datos_meses[mes]['ingresos'] += t.monto
        else:
            datos_meses[mes]['gastos'] += t.monto

    meses = sorted(datos_meses.keys())
    ingresos = [datos_meses[m]['ingresos'] for m in meses]
    gastos = [datos_meses[m]['gastos'] for m in meses]

    # Gastos por categoria
    categorias_lista = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    montos_categorias = [sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.categoria == cat) for cat in categorias_lista]

    # Evolucion del balance
    balance = 0
    balances = []
    fechas = []
    for t in transacciones:
        if t.tipo == 'ingreso':
            balance += t.monto
        else:
            balance -= t.monto
        balances.append(round(balance, 2))
        fechas.append(t.fecha.strftime('%d/%m/%Y'))

    return render_template('graficas.html',
        meses=meses,
        ingresos=ingresos,
        gastos=gastos,
        categorias=categorias_lista,
        montos_categorias=montos_categorias,
        balances=balances,
        fechas=fechas
    )

@app.route('/categorias')
@login_required
def categorias():
    categorias = Categoria.query.filter_by(usuario_id=current_user.id).all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/agregar', methods=['POST'])
@login_required
def agregar_categoria():
    nombre = request.form['nombre'].strip()
    icono = request.form['icono'].strip()

    if len(nombre) < 2:
        flash('El nombre debe tener al menos 2 caracteres')
        return redirect(url_for('categorias'))

    if Categoria.query.filter_by(usuario_id=current_user.id, nombre=nombre).first():
        flash('Ya tienes una categoría con ese nombre')
        return redirect(url_for('categorias'))

    nueva = Categoria(nombre=nombre, icono=icono, usuario_id=current_user.id)
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route('/categorias/eliminar/<int:id>')
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if categoria.usuario_id != current_user.id:
        return redirect(url_for('categorias'))
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route('/idioma/<lang>')
@login_required
def cambiar_idioma(lang):
    if lang in ['es', 'en']:
        current_user.idioma = lang
        db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/recurrentes')
@login_required
def recurrentes():
    recurrentes = Recurrente.query.filter_by(usuario_id=current_user.id).all()
    return render_template('recurrentes.html', recurrentes=recurrentes)

@app.route('/recurrentes/agregar', methods=['POST'])
@login_required
def agregar_recurrente():
    nueva = Recurrente(
        descripcion=request.form['descripcion'],
        monto=float(request.form['monto']),
        tipo=request.form['tipo'],
        categoria=request.form['categoria'],
        dia=int(request.form['dia']),
        usuario_id=current_user.id
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('recurrentes'))

@app.route('/recurrentes/eliminar/<int:id>')
@login_required
def eliminar_recurrente(id):
    recurrente = Recurrente.query.get_or_404(id)
    if recurrente.usuario_id != current_user.id:
        return redirect(url_for('recurrentes'))
    db.session.delete(recurrente)
    db.session.commit()
    return redirect(url_for('recurrentes'))

@app.route('/recurrentes/procesar')
@login_required
def procesar_recurrentes():
    from datetime import datetime
    hoy = datetime.now()
    recurrentes = Recurrente.query.filter_by(usuario_id=current_user.id).all()
    agregadas = 0

    for r in recurrentes:
        if r.dia == hoy.day:
            ya_existe = Transaccion.query.filter_by(
                usuario_id=current_user.id,
                descripcion=r.descripcion,
                monto=r.monto
            ).filter(
                db.func.strftime('%Y-%m-%d', Transaccion.fecha) == hoy.strftime('%Y-%m-%d')
            ).first()

            if not ya_existe:
                nueva = Transaccion(
                    descripcion=r.descripcion,
                    monto=r.monto,
                    tipo=r.tipo,
                    categoria=r.categoria,
                    usuario_id=current_user.id
                )
                db.session.add(nueva)
                agregadas += 1

    db.session.commit()
    flash(f'{agregadas} transacciones recurrentes procesadas')
    return redirect(url_for('index'))

@app.route('/buscar')
@login_required
def buscar():
    query_texto = request.args.get('q', '')
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    tipo_filtro = request.args.get('tipo', '')

    query = Transaccion.query.filter_by(usuario_id=current_user.id)

    if query_texto:
        query = query.filter(Transaccion.descripcion.ilike(f'%{query_texto}%'))

    if tipo_filtro:
        query = query.filter_by(tipo=tipo_filtro)

    if fecha_inicio:
        from datetime import datetime
        query = query.filter(Transaccion.fecha >= datetime.strptime(fecha_inicio, '%Y-%m-%d'))

    if fecha_fin:
        from datetime import datetime
        query = query.filter(Transaccion.fecha <= datetime.strptime(fecha_fin, '%Y-%m-%d'))

    resultados = query.order_by(Transaccion.fecha.desc()).all()
    total = sum(t.monto if t.tipo == 'ingreso' else -t.monto for t in resultados)

    return render_template('buscar.html',
        resultados=resultados,
        total=round(total, 2),
        q=query_texto,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        tipo_filtro=tipo_filtro
    )

@app.route('/metas')
@login_required
def metas():
    metas = Meta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('metas.html', metas=metas)

@app.route('/metas/agregar', methods=['POST'])
@login_required
def agregar_meta():
    from datetime import datetime
    fecha_limite = request.form.get('fecha_limite')
    nueva = Meta(
        nombre=request.form['nombre'],
        monto_objetivo=float(request.form['monto_objetivo']),
        fecha_limite=datetime.strptime(fecha_limite, '%Y-%m-%d') if fecha_limite else None,
        usuario_id=current_user.id
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('metas'))

@app.route('/metas/abonar/<int:id>', methods=['POST'])
@login_required
def abonar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return redirect(url_for('metas'))
    monto = float(request.form['monto'])
    meta.monto_actual += monto
    if meta.monto_actual >= meta.monto_objetivo:
        meta.completada = True
    db.session.commit()
    return redirect(url_for('metas'))

@app.route('/metas/eliminar/<int:id>')
@login_required
def eliminar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return redirect(url_for('metas'))
    db.session.delete(meta)
    db.session.commit()
    return redirect(url_for('metas'))

@app.route('/reporte')
@login_required
def reporte():
    from datetime import datetime
    import io

    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).order_by(Transaccion.fecha.desc()).all()
    ingresos = sum(t.monto for t in transacciones if t.tipo == 'ingreso')
    gastos = sum(t.monto for t in transacciones if t.tipo == 'gasto')
    balance = ingresos - gastos

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    elementos.append(Paragraph('Reporte de Finanzas Personales', styles['Title']))
    elementos.append(Paragraph(f'Usuario: {current_user.username}', styles['Normal']))
    elementos.append(Paragraph(f'Fecha: {datetime.now().strftime("%d/%m/%Y")}', styles['Normal']))
    elementos.append(Spacer(1, 20))

    # Resumen
    elementos.append(Paragraph('Resumen General', styles['Heading2']))
    resumen_data = [
        ['Concepto', 'Monto'],
        ['Total Ingresos', f'${round(ingresos, 2)}'],
        ['Total Gastos', f'${round(gastos, 2)}'],
        ['Balance', f'${round(balance, 2)}'],
    ]
    tabla_resumen = Table(resumen_data, colWidths=[300, 150])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 20))

    # Historial
    elementos.append(Paragraph('Historial de Transacciones', styles['Heading2']))
    datos = [['Descripción', 'Monto', 'Tipo', 'Categoría', 'Fecha']]
    for t in transacciones:
        datos.append([
            t.descripcion,
            f'${t.monto}',
            t.tipo,
            t.categoria,
            t.fecha.strftime('%d/%m/%Y')
        ])

    tabla = Table(datos, colWidths=[150, 80, 70, 100, 80])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabla)

    doc.build(elementos)
    buffer.seek(0)

    return send_file(buffer, download_name=f'reporte_{datetime.now().strftime("%Y%m%d")}.pdf', as_attachment=True, mimetype='application/pdf')

@app.route('/moneda', methods=['GET', 'POST'])
@login_required
def moneda():
    if request.method == 'POST':
        current_user.moneda = request.form['moneda']
        db.session.commit()
        flash('Moneda actualizada exitosamente')
        return redirect(url_for('index'))
    return render_template('moneda.html')

if __name__ == '__main__':
    app.run(debug=True)