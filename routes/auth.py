from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario
from itsdangerous import URLSafeTimedSerializer

auth = Blueprint('auth', __name__)

def get_serializer():
    from flask import current_app
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if len(username) < 3:
            flash('El usuario debe tener al menos 3 caracteres')
            return redirect(url_for('auth.registro'))

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres')
            return redirect(url_for('auth.registro'))

        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe')
            return redirect(url_for('auth.registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado')
            return redirect(url_for('auth.registro'))

        nuevo = Usuario(username=username, email=email, password=generate_password_hash(password))
        db.session.add(nuevo)
        db.session.commit()

        try:
            from flask_mail import Message
            from flask import current_app
            from extensions import mail # type: ignore
            msg = Message('Bienvenido a Mis Finanzas',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email])
            msg.body = f'Hola {username}, tu cuenta fue creada exitosamente. ¡Bienvenido!'
            mail.send(msg)
        except:
            pass

        flash('Cuenta creada exitosamente, inicia sesión')
        return redirect(url_for('auth.login'))
    return render_template('registro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(username=request.form['username']).first()
        if usuario and check_password_hash(usuario.password, request.form['password']):
            if usuario.otp_activo:
                from flask import session
                session['usuario_pendiente'] = usuario.id
                return redirect(url_for('auth.verificar_login_2fa'))
            login_user(usuario)
            return redirect(url_for('finanzas.index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@auth.route('/login/2fa', methods=['GET', 'POST'])
def verificar_login_2fa():
    from flask import session
    import pyotp
    if 'usuario_pendiente' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        usuario = Usuario.query.get(session['usuario_pendiente'])
        codigo = request.form['codigo']
        totp = pyotp.TOTP(usuario.otp_secret)
        if totp.verify(codigo):
            session.pop('usuario_pendiente')
            login_user(usuario)
            return redirect(url_for('finanzas.index'))
        flash('Código incorrecto')
    return render_template('2fa_login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email'].strip()
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            serializer = get_serializer()
            token = serializer.dumps(email, salt='recuperar-password')
            enlace = url_for('auth.restablecer', token=token, _external=True)
            try:
                from flask_mail import Message
                from flask import current_app
                from extensions import mail
                msg = Message('Recuperar contraseña',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[email])
                msg.body = f'Hola {usuario.username}, haz clic en este enlace:\n\n{enlace}\n\nExpira en 30 minutos.'
                mail.send(msg)
            except:
                pass
        flash('Si el correo existe recibirás un enlace')
        return redirect(url_for('auth.login'))
    return render_template('recuperar.html')

@auth.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer(token):
    try:
        serializer = get_serializer()
        email = serializer.loads(token, salt='recuperar-password', max_age=1800)
    except:
        flash('El enlace ha expirado o no es válido')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form['password']
        confirmar = request.form['confirmar']

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres')
            return redirect(url_for('auth.restablecer', token=token))

        if password != confirmar:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('auth.restablecer', token=token))

        usuario = Usuario.query.filter_by(email=email).first()
        usuario.password = generate_password_hash(password)
        db.session.commit()
        flash('Contraseña restablecida exitosamente')
        return redirect(url_for('auth.login'))

    return render_template('restablecer.html', token=token)