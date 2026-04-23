from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models import db, Transaccion, Presupuesto, Categoria
from datetime import datetime
import io

finanzas = Blueprint('finanzas', __name__)

@finanzas.route('/')
@login_required
def index():
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

    ingresos_total = sum(t.monto for t in todas if t.tipo == 'ingreso')
    gastos_total = sum(t.monto for t in todas if t.tipo == 'gasto')
    balance = ingresos_total - gastos_total

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

@finanzas.route('/agregar', methods=['POST'])
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
                    from flask_mail import Message
                    from flask import current_app
                    from extensions import mail
                    msg = Message('⚠️ Alerta de presupuesto',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=[current_user.email])
                    msg.body = f'''Hola {current_user.username},
Has usado el {round(porcentaje)}% de tu presupuesto de {nueva.categoria}.
Presupuesto: ${presupuesto.monto}
Gastado: ${round(gastado, 2)}
Disponible: ${round(presupuesto.monto - gastado, 2)}'''
                    mail.send(msg)
                except:
                    pass

    return redirect(url_for('finanzas.index'))

@finanzas.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    transaccion = Transaccion.query.get_or_404(id)
    if transaccion.usuario_id != current_user.id:
        return redirect(url_for('finanzas.index'))
    db.session.delete(transaccion)
    db.session.commit()
    return redirect(url_for('finanzas.index'))

@finanzas.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    transaccion = Transaccion.query.get_or_404(id)
    if transaccion.usuario_id != current_user.id:
        return redirect(url_for('finanzas.index'))
    if request.method == 'POST':
        transaccion.descripcion = request.form['descripcion']
        transaccion.monto = float(request.form['monto'])
        transaccion.tipo = request.form['tipo']
        transaccion.categoria = request.form['categoria']
        db.session.commit()
        return redirect(url_for('finanzas.index'))
    return render_template('editar.html', transaccion=transaccion)

@finanzas.route('/exportar')
@login_required
def exportar():
    import openpyxl
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

@finanzas.route('/reporte')
@login_required
def reporte():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).order_by(Transaccion.fecha.desc()).all()
    ingresos = sum(t.monto for t in transacciones if t.tipo == 'ingreso')
    gastos = sum(t.monto for t in transacciones if t.tipo == 'gasto')
    balance = ingresos - gastos

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph('Reporte de Finanzas Personales', styles['Title']))
    elementos.append(Paragraph(f'Usuario: {current_user.username}', styles['Normal']))
    elementos.append(Paragraph(f'Fecha: {datetime.now().strftime("%d/%m/%Y")}', styles['Normal']))
    elementos.append(Spacer(1, 20))

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

    elementos.append(Paragraph('Historial de Transacciones', styles['Heading2']))
    datos = [['Descripción', 'Monto', 'Tipo', 'Categoría', 'Fecha']]
    for t in transacciones:
        datos.append([t.descripcion, f'${t.monto}', t.tipo, t.categoria, t.fecha.strftime('%d/%m/%Y')])

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

@finanzas.route('/resumen')
@login_required
def resumen():
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

@finanzas.route('/graficas')
@login_required
def graficas():
    transacciones = Transaccion.query.filter_by(usuario_id=current_user.id).order_by(Transaccion.fecha).all()
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

    categorias_lista = ['comida', 'transporte', 'entretenimiento', 'salud', 'otros']
    montos_categorias = [sum(t.monto for t in transacciones if t.tipo == 'gasto' and t.categoria == cat) for cat in categorias_lista]

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
        meses=meses, ingresos=ingresos, gastos=gastos,
        categorias=categorias_lista, montos_categorias=montos_categorias,
        balances=balances, fechas=fechas)

@finanzas.route('/buscar')
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
        query = query.filter(Transaccion.fecha >= datetime.strptime(fecha_inicio, '%Y-%m-%d'))
    if fecha_fin:
        query = query.filter(Transaccion.fecha <= datetime.strptime(fecha_fin, '%Y-%m-%d'))

    resultados = query.order_by(Transaccion.fecha.desc()).all()
    total = sum(t.monto if t.tipo == 'ingreso' else -t.monto for t in resultados)

    return render_template('buscar.html',
        resultados=resultados, total=round(total, 2),
        q=query_texto, fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin, tipo_filtro=tipo_filtro)