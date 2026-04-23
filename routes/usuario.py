from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Presupuesto, Transaccion
from datetime import datetime

usuario = Blueprint('usuario', __name__)

@usuario.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@usuario.route('/perfil/username', methods=['POST'])
@login_required
def cambiar_username():
    from models import Usuario as UsuarioModel
    username = request.form['username'].strip()
    if len(username) < 3:
        flash('El usuario debe tener al menos 3 caracteres', 'username')
        return redirect(url_for('usuario.perfil'))
    if UsuarioModel.query.filter_by(username=username).first():
        flash('Ese usuario ya existe', 'username')
        return redirect(url_for('usuario.perfil'))
    current_user.username = username
    db.session.commit()
    flash('Usuario actualizado exitosamente', 'username')
    return redirect(url_for('usuario.perfil'))

@usuario.route('/perfil/password', methods=['POST'])
@login_required
def cambiar_password():
    password_actual = request.form['password_actual']
    password_nuevo = request.form['password_nuevo']
    password_confirmar = request.form['password_confirmar']
    if not check_password_hash(current_user.password, password_actual):
        flash('La contraseña actual es incorrecta', 'password')
        return redirect(url_for('usuario.perfil'))
    if len(password_nuevo) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres', 'password')
        return redirect(url_for('usuario.perfil'))
    if password_nuevo != password_confirmar:
        flash('Las contraseñas no coinciden', 'password')
        return redirect(url_for('usuario.perfil'))
    current_user.password = generate_password_hash(password_nuevo)
    db.session.commit()
    flash('Contraseña actualizada exitosamente', 'password')
    return redirect(url_for('usuario.perfil'))

@usuario.route('/moneda', methods=['GET', 'POST'])
@login_required
def moneda():
    if request.method == 'POST':
        current_user.moneda = request.form['moneda']
        db.session.commit()
        flash('Moneda actualizada exitosamente')
        return redirect(url_for('finanzas.index'))
    return render_template('moneda.html')

@usuario.route('/presupuesto')
@login_required
def presupuesto():
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

@usuario.route('/presupuesto/guardar', methods=['POST'])
@login_required
def guardar_presupuesto():
    mes_actual = datetime.now().strftime('%Y-%m')
    categorias = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
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
    return redirect(url_for('usuario.presupuesto'))

@usuario.route('/2fa/activar')
@login_required
def activar_2fa():
    import pyotp
    import qrcode
    import io
    import base64

    if not current_user.otp_secret:
        current_user.otp_secret = pyotp.random_base32()
        db.session.commit()

    totp = pyotp.TOTP(current_user.otp_secret)
    uri = totp.provisioning_uri(current_user.email, issuer_name='Mis Finanzas')

    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template('2fa_activar.html', qr=qr_base64, secret=current_user.otp_secret)

@usuario.route('/2fa/verificar', methods=['POST'])
@login_required
def verificar_2fa():
    import pyotp
    codigo = request.form['codigo']
    totp = pyotp.TOTP(current_user.otp_secret)
    if totp.verify(codigo):
        current_user.otp_activo = True
        db.session.commit()
        flash('2FA activado exitosamente')
    else:
        flash('Código incorrecto, intenta de nuevo')
    return redirect(url_for('usuario.activar_2fa'))

@usuario.route('/2fa/desactivar')
@login_required
def desactivar_2fa():
    current_user.otp_activo = False
    current_user.otp_secret = None
    db.session.commit()
    flash('2FA desactivado')
    return redirect(url_for('usuario.perfil'))