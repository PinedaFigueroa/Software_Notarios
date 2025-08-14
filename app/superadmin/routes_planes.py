# archivo: app/superadmin/routes_planes.py
# última actualización: 13/08/25 hora 02:39
# autor: Giancarlo + Tars-90
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import superadmin_bp
from .forms_planes import PlanForm

try:
    from app.models.core import db
except Exception:
    from app.core_ext import db

from app.models.planes import Plan
from app.models.bufetes import BufeteJuridico

@superadmin_bp.route('/superadmin/planes')
@login_required
def planes_listar():
    page = request.args.get('page', 1, type=int)
    q = Plan.query.order_by(Plan.activo.desc(), Plan.nombre.asc())
    planes = q.paginate(page=page, per_page=25, error_out=False)
    return render_template('superadmin/planes/listar_planes.html', planes=planes)

@superadmin_bp.route('/superadmin/planes/nuevo', methods=['GET', 'POST'])
@login_required
def plan_nuevo():
    form = PlanForm()
    if form.validate_on_submit():
        if Plan.query.filter_by(nombre=form.nombre.data).first():
            flash('Ya existe un plan con ese nombre.', 'warning')
            return render_template('superadmin/planes/form_plan.html', form=form, modo='crear')
        p = Plan(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data or None,
            max_notarios=form.max_notarios.data,
            max_procuradores=form.max_procuradores.data,
            max_asistentes=form.max_asistentes.data,
            max_documentos=form.max_documentos.data,
            storage_mb=form.storage_mb.data,
            precio_mensual=float(form.precio_mensual.data or 0),
            es_personalizado=bool(form.es_personalizado.data),
            activo=bool(form.activo.data)
        )
        db.session.add(p)
        db.session.commit()
        flash('Plan creado', 'success')
        return redirect(url_for('superadmin.planes_listar'))
    return render_template('superadmin/planes/form_plan.html', form=form, modo='crear')

@superadmin_bp.route('/superadmin/planes/<int:plan_id>/editar', methods=['GET', 'POST'])
@login_required
def plan_editar(plan_id):
    p = Plan.query.get_or_404(plan_id)
    form = PlanForm(obj=p)
    if form.validate_on_submit():
        # Verificar nombre único para otros
        existe = Plan.query.filter(Plan.id != p.id, Plan.nombre == form.nombre.data).first()
        if existe:
            flash('Ese nombre ya está en uso por otro plan.', 'warning')
            return render_template('superadmin/planes/form_plan.html', form=form, modo='editar', plan=p)
        p.nombre = form.nombre.data
        p.descripcion = form.descripcion.data or None
        p.max_notarios = form.max_notarios.data
        p.max_procuradores = form.max_procuradores.data
        p.max_asistentes = form.max_asistentes.data
        p.max_documentos = form.max_documentos.data
        p.storage_mb = form.storage_mb.data
        p.precio_mensual = float(form.precio_mensual.data or 0)
        p.es_personalizado = bool(form.es_personalizado.data)
        p.activo = bool(form.activo.data)
        db.session.commit()
        flash('Plan actualizado', 'success')
        return redirect(url_for('superadmin.planes_listar'))
    return render_template('superadmin/planes/form_plan.html', form=form, modo='editar', plan=p)

@superadmin_bp.route('/superadmin/planes/<int:plan_id>/eliminar', methods=['POST'])
@login_required
def plan_eliminar(plan_id):
    p = Plan.query.get_or_404(plan_id)
    # Si tiene bufetes, no permitir eliminar; solo desactivar
    tiene_bufetes = db.session.query(BufeteJuridico.id).filter_by(plan_id=p.id, activo=True).first() is not None
    if tiene_bufetes:
        p.activo = False
        db.session.commit()
        flash('Plan desactivado (tiene bufetes asociados).', 'warning')
    else:
        db.session.delete(p)
        db.session.commit()
        flash('Plan eliminado.', 'success')
    return redirect(url_for('superadmin.planes_listar'))
