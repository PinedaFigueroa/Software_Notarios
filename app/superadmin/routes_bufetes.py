# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 09 / 08 / 25
# cantidad de lineas originales: 220
# última actualización: 12 / 08 / 25 hora 03:25
# motivo de la actualización: CRUD real de Bufetes (listar/buscar, crear, editar, toggle activo)
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""Rutas de gestión de Bufetes para SuperAdmin."""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

from app.core_ext import db  # alias estable

# Modelos con import flexible
BufeteJuridico = None
try:
    from app.models.usuarios import BufeteJuridico  # opción 1
except Exception:
    try:
        from app.models.bufetes import BufeteJuridico  # opción 2
    except Exception:
        pass

from .forms_bufetes import BufeteForm

@superadmin_bp.route('/superadmin/bufetes')
@login_required
@rol_required(['SUPERADMIN'])
def listar_bufetes():
    q = request.args.get('q', type=str, default='')
    query = BufeteJuridico.query if BufeteJuridico else None
    bufetes = []
    if query is not None:
        if q:
            query = query.filter(BufeteJuridico.nombre_bufete.ilike(f"%{q}%"))
        bufetes = query.order_by(BufeteJuridico.id.asc()).all()
    return render_template('superadmin/bufetes/listar_bufetes.html', bufetes=bufetes, q=q)

@superadmin_bp.route('/superadmin/bufetes/nuevo', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def crear_bufete():
    form = BufeteForm()
    form.refresh_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            plan_id = form.plan_id.data or None
            if plan_id == '':
                plan_id = None
            obj = BufeteJuridico(
                nombre_bufete=form.nombre_bufete.data.strip(),
                plan_id=int(plan_id) if plan_id else None,
                activo=bool(form.activo.data),
            )
            db.session.add(obj)
            db.session.commit()
            flash('Bufete creado correctamente.', 'success')
            return redirect(url_for('superadmin_bp.listar_bufetes'))
        else:
            flash('Por favor corrige los errores del formulario.', 'danger')
    return render_template('superadmin/bufetes/form_bufete.html', titulo='Crear Bufete', form=form)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/editar', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def editar_bufete(bufete_id):
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    form = BufeteForm(obj=bufete)
    form.refresh_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            plan_id = form.plan_id.data or None
            if plan_id == '':
                plan_id = None
            bufete.nombre_bufete = form.nombre_bufete.data.strip()
            bufete.plan_id = int(plan_id) if plan_id else None
            bufete.activo = bool(form.activo.data)
            db.session.add(bufete)
            db.session.commit()
            flash('Bufete actualizado correctamente.', 'success')
            return redirect(url_for('superadmin_bp.listar_bufetes'))
        else:
            flash('Por favor corrige los errores del formulario.', 'danger')
    form.plan_id.data = str(bufete.plan_id) if bufete.plan_id else ''
    return render_template('superadmin/bufetes/form_bufete.html', titulo=f'Editar: {bufete.nombre_bufete}', form=form, bufete=bufete)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/toggle', methods=['POST'])
@login_required
@rol_required(['SUPERADMIN'])
def toggle_estado_bufete(bufete_id):
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    bufete.activo = not bool(bufete.activo)
    db.session.add(bufete)
    db.session.commit()
    flash(f"Bufete '{bufete.nombre_bufete}' ahora está {'activo' if bufete.activo else 'inactivo'}.", 'success')
    next_url = url_for('superadmin_bp.listar_bufetes', q=request.args.get('q', ''))
    return redirect(next_url)
