from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario
from validators import validar_registro, validar_email, validar_contraseña
from extensions import limiter
from itsdangerous import URLSafeTimedSerializer
import logging

auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def get_serializer():
    from flask import current_app
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth.route('/registro', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # 5 registros por minuto
def registro():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirmar_password = request.form.get('confirmar_password', '')
        
        # Validar que las contraseñas coincidan
        if password != confirmar_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.registro'))
        
        # Validar todos los campos
        resultado = validar_registro(username, email, password)
        if not resultado['valido']:
            for error in resultado['errores']:
                flash(error, 'error')
            return redirect(url_for('auth.registro'))
        
        # Verificar si el usuario o email ya existen
        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado', 'error')
            return redirect(url_for('auth.registro'))
        
        try:
            nuevo = Usuario(username=username, email=email, password=generate_password_hash(password))
            db.session.add(nuevo)
            db.session.commit()
            
            # Intentar enviar email de bienvenida
            try:
                from flask_mail import Message
                from flask import current_app
                from extensions import mail
                msg = Message('Bienvenido a Mis Finanzas',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[email])
                msg.body = f'Hola {username}, tu cuenta fue creada exitosamente. ¡Bienvenido!'
                mail.send(msg)
                logger.info(f'Email de bienvenida enviado a {email}')
            except Exception as e:
                logger.warning(f'No se pudo enviar email a {email}: {str(e)}')
            
            flash('Cuenta creada exitosamente, inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error al registrar usuario: {str(e)}')
            flash('Error al crear la cuenta. Intenta nuevamente', 'error')
            return redirect(url_for('auth.registro'))
    
    return render_template('registro.html')

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # 5 intentos de login por minuto
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Usuario y contraseña son requeridos', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            usuario = Usuario.query.filter_by(username=username).first()
            if usuario and check_password_hash(usuario.password, password):
                if usuario.otp_activo:
                    from flask import session
                    session['usuario_pendiente'] = usuario.id
                    logger.info(f'Login con 2FA iniciado para {username}')
                    return redirect(url_for('auth.verificar_login_2fa'))
                login_user(usuario)
                logger.info(f'Login exitoso para {username}')
                return redirect(url_for('finanzas.index'))
            
            # No especificar si el usuario o la contraseña es incorrecta (seguridad)
            logger.warning(f'Intento de login fallido para {username}')
            flash('Usuario o contraseña incorrectos', 'error')
        except Exception as e:
            logger.error(f'Error en login: {str(e)}')
            flash('Error al iniciar sesión', 'error')
    
    return render_template('login.html')

@auth.route('/login/2fa', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # 10 intentos 2FA por minuto
def verificar_login_2fa():
    from flask import session
    import pyotp
    
    if 'usuario_pendiente' not in session:
        logger.warning('Intento de acceso a 2FA sin usuario pendiente')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            usuario = Usuario.query.get(session['usuario_pendiente'])
            if not usuario:
                logger.error('Usuario pendiente no encontrado')
                return redirect(url_for('auth.login'))
            
            codigo = request.form.get('codigo', '').strip()
            if not codigo:
                flash('Ingresa el código de autenticación', 'error')
                return redirect(url_for('auth.verificar_login_2fa'))
            
            totp = pyotp.TOTP(usuario.otp_secret)
            if totp.verify(codigo):
                session.pop('usuario_pendiente')
                login_user(usuario)
                logger.info(f'Login 2FA exitoso para {usuario.username}')
                return redirect(url_for('finanzas.index'))
            
            logger.warning(f'Código 2FA incorrecto para {usuario.username}')
            flash('Código incorrecto', 'error')
        except Exception as e:
            logger.error(f'Error en verificación 2FA: {str(e)}')
            flash('Error al verificar código', 'error')
    
    return render_template('2fa_login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/recuperar', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # 5 intentos de recuperación por minuto
def recuperar():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        # Validar que el email tenga formato correcto
        email_valido, err_email = validar_email(email)
        if not email_valido:
            logger.warning(f'Intento de recuperación con email inválido: {email}')
            flash('Por favor ingresa un email válido', 'error')
            return redirect(url_for('auth.recuperar'))
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            try:
                serializer = get_serializer()
                token = serializer.dumps(email, salt='recuperar-password')
                enlace = url_for('auth.restablecer', token=token, _external=True)
                
                from flask_mail import Message
                from flask import current_app
                from extensions import mail
                msg = Message('Recuperar contraseña',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[email])
                msg.body = f'Hola {usuario.username}, haz clic en este enlace para recuperar tu contraseña:\n\n{enlace}\n\nEste enlace expira en 30 minutos.'
                mail.send(msg)
                logger.info(f'Email de recuperación enviado a {email}')
            except Exception as e:
                logger.error(f'Error enviando email de recuperación a {email}: {str(e)}')
        else:
            logger.info(f'Intento de recuperación con email no registrado: {email}')
        
        # No revelar si el email existe o no (seguridad)
        flash('Si el correo existe en nuestra base de datos, recibirás un enlace de recuperación', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('recuperar.html')

@auth.route('/restablecer/<token>', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # 5 intentos de restablecimiento por minuto
def restablecer(token):
    try:
        serializer = get_serializer()
        email = serializer.loads(token, salt='recuperar-password', max_age=1800)
    except Exception as e:
        logger.warning(f'Intento de restablecer con token inválido: {str(e)}')
        flash('El enlace ha expirado o no es válido', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar', '')

        # Validar que las contraseñas coincidan
        if password != confirmar:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.restablecer', token=token))

        # Validar que la contraseña sea fuerte
        contraseña_valida, err_contraseña = validar_contraseña(password)
        if not contraseña_valida:
            flash(err_contraseña, 'error')
            return redirect(url_for('auth.restablecer', token=token))

        try:
            usuario = Usuario.query.filter_by(email=email).first()
            if not usuario:
                logger.error(f'Usuario no encontrado para email: {email}')
                flash('Error al restablecer contraseña', 'error')
                return redirect(url_for('auth.login'))
            
            usuario.password = generate_password_hash(password)
            db.session.commit()
            logger.info(f'Contraseña restablecida para {email}')
            flash('Contraseña restablecida exitosamente. Inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error restableciendo contraseña: {str(e)}')
            flash('Error al restablecer contraseña', 'error')
            return redirect(url_for('auth.restablecer', token=token))

    return render_template('restablecer.html', token=token)