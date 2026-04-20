from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Transaccion

from flask_mail import Mail, Message

from flask import send_file
import openpyxl
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_123'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'martinezmestrajuanpablo7@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxpf lxqu slti jidv'

mail = Mail(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()

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

    categorias_lista = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    montos_lista = [sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.categoria == cat) for cat in categorias_lista]

    return render_template('index.html',
        transacciones=transacciones,
        balance=round(balance, 2),
        categorias=categorias_lista,
        montos=montos_lista,
        filtro=categoria_filtro,
        fecha_filtro=fecha_filtro
    )

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    nueva = Transaccion(
        descripcion=request.form['descripcion'],
        monto=float(request.form['monto']),
        tipo=request.form['tipo'],
        categoria=request.form['categoria'],
        usuario_id=current_user.id
    )
    db.session.add(nueva)
    db.session.commit()
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

if __name__ == '__main__':
    app.run(debug=True)