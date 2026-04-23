from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaccion, Categoria, Recurrente, Meta
from datetime import datetime

extras = Blueprint('extras', __name__)

@extras.route('/categorias')
@login_required
def categorias():
    cats = Categoria.query.filter_by(usuario_id=current_user.id).all()
    return render_template('categorias.html', categorias=cats)

@extras.route('/categorias/agregar', methods=['POST'])
@login_required
def agregar_categoria():
    nombre = request.form['nombre'].strip()
    icono = request.form['icono'].strip()
    if len(nombre) < 2:
        flash('El nombre debe tener al menos 2 caracteres')
        return redirect(url_for('extras.categorias'))
    if Categoria.query.filter_by(usuario_id=current_user.id, nombre=nombre).first():
        flash('Ya tienes una categoría con ese nombre')
        return redirect(url_for('extras.categorias'))
    nueva = Categoria(nombre=nombre, icono=icono, usuario_id=current_user.id)
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('extras.categorias'))

@extras.route('/categorias/eliminar/<int:id>')
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if categoria.usuario_id != current_user.id:
        return redirect(url_for('extras.categorias'))
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('extras.categorias'))

@extras.route('/recurrentes')
@login_required
def recurrentes():
    recs = Recurrente.query.filter_by(usuario_id=current_user.id).all()
    return render_template('recurrentes.html', recurrentes=recs)

@extras.route('/recurrentes/agregar', methods=['POST'])
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
    return redirect(url_for('extras.recurrentes'))

@extras.route('/recurrentes/eliminar/<int:id>')
@login_required
def eliminar_recurrente(id):
    recurrente = Recurrente.query.get_or_404(id)
    if recurrente.usuario_id != current_user.id:
        return redirect(url_for('extras.recurrentes'))
    db.session.delete(recurrente)
    db.session.commit()
    return redirect(url_for('extras.recurrentes'))

@extras.route('/recurrentes/procesar')
@login_required
def procesar_recurrentes():
    hoy = datetime.now()
    recs = Recurrente.query.filter_by(usuario_id=current_user.id).all()
    agregadas = 0
    for r in recs:
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
    return redirect(url_for('finanzas.index'))

@extras.route('/metas')
@login_required
def metas():
    mts = Meta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('metas.html', metas=mts)

@extras.route('/metas/agregar', methods=['POST'])
@login_required
def agregar_meta():
    fecha_limite = request.form.get('fecha_limite')
    nueva = Meta(
        nombre=request.form['nombre'],
        monto_objetivo=float(request.form['monto_objetivo']),
        fecha_limite=datetime.strptime(fecha_limite, '%Y-%m-%d') if fecha_limite else None,
        usuario_id=current_user.id
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect(url_for('extras.metas'))

@extras.route('/metas/abonar/<int:id>', methods=['POST'])
@login_required
def abonar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return redirect(url_for('extras.metas'))
    monto = float(request.form['monto'])
    meta.monto_actual += monto
    if meta.monto_actual >= meta.monto_objetivo:
        meta.completada = True
    db.session.commit()
    return redirect(url_for('extras.metas'))

@extras.route('/metas/eliminar/<int:id>')
@login_required
def eliminar_meta(id):
    meta = Meta.query.get_or_404(id)
    if meta.usuario_id != current_user.id:
        return redirect(url_for('extras.metas'))
    db.session.delete(meta)
    db.session.commit()
    return redirect(url_for('extras.metas'))