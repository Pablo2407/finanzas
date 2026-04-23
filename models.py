from extensions import db
from flask_login import UserMixin



class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    idioma = db.Column(db.String(5), default='es')
    moneda = db.Column(db.String(10), default='$')
    push_suscripcion = db.Column(db.Text, nullable=True)
    otp_secret = db.Column(db.String(32), nullable=True)
    otp_activo = db.Column(db.Boolean, default=False)
    transacciones = db.relationship('Transaccion', backref='usuario', lazy=True)

class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    categoria = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Presupuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    mes = db.Column(db.String(7), nullable=False)  # formato: 2026-04
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    icono = db.Column(db.String(10), default='🏷️')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Recurrente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    categoria = db.Column(db.String(50))
    dia = db.Column(db.Integer, nullable=False)  # dia del mes que se repite
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    monto_objetivo = db.Column(db.Float, nullable=False)
    monto_actual = db.Column(db.Float, default=0)
    fecha_limite = db.Column(db.DateTime, nullable=True)
    completada = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)