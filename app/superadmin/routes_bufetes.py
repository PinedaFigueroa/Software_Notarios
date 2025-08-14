# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 2025-08-13
# última actualización: 2025-08-13 | motivo: CRUD completo + plan_id + evitar circular import
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import superadmin_bp                     # ✅ usar el blueprint
from .forms_bufetes import BufeteForm
from app import db                              # usar la instancia global
from app.models.bufetes import BufeteJuridico
from app.models.planes import Plan

def _choices_planes():
    return [(p.id, p.nombre) for p in Plan.query.filter_by(activo=True).order_by(Plan.nombre.asc()).all()]

@superadmin_bp.route('/superadmin/bufetes')
@login_required
def listar_bufetes():
    page = request.args.get('page', 1, type=int)
    q = BufeteJuridico.query.order_by(BufeteJuridico.nombre_bufete.asc())
    bufetes = q.paginate(page=page, per_page=25, error_out=False)
    return render_template('superadmin/bufetes/listar_bufetes.html', bufetes=bufetes)

@superadmin_bp.route('/superadmin/bufetes/nuevo', methods=['GET', 'POST'])
@login_required
def crear_bufete():
    form = BufeteForm()
    form.plan_id.choices = _choices_planes()    # ✅ importante
    if form.validate_on_submit():
        b = BufeteJuridico(
            nombre_bufete=form.nombre_bufete.data.strip(),
            direccion=form.direccion.data or None,
            telefono=form.telefono.data or None,
            email=form.email.data or None,
            nit=form.nit.data or None,
            pais=form.pais.data or None,
            forma_contacto=form.forma_contacto.data or None,
            facturacion_nombre=form.facturacion_nombre.data or None,
            facturacion_nit=form.facturacion_nit.data or None,
            facturacion_direccion=form.facturacion_direccion.data or None,
            formas_pago=form.formas_pago.data or None,
            metodo_pago_preferido=form.metodo_pago_preferido.data or None,
            maneja_inventario_timbres_papel=bool(form.maneja_inventario_timbres_papel.data),
            incluye_libreria_plantillas_inicial=bool(form.incluye_libreria_plantillas_inicial.data),
            habilita_auditoria_borrado_logico=bool(form.habilita_auditoria_borrado_logico.data),
            habilita_dashboard_avanzado=bool(form.habilita_dashboard_avanzado.data),
            habilita_ayuda_contextual=bool(form.habilita_ayuda_contextual.data),
            habilita_papeleria_digital=bool(form.habilita_papeleria_digital.data),
            plan_id=form.plan_id.data,
            activo=True
        )
        db.session.add(b)
        db.session.commit()
        flash('Bufete creado', 'success')
        return redirect(url_for('superadmin.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='crear')

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_bufete(bufete_id):
    b = BufeteJuridico.query.get_or_404(bufete_id)
    form = BufeteForm(obj=b)
    form.plan_id.choices = _choices_planes()    # ✅ importante
    if form.validate_on_submit():
        b.nombre_bufete = form.nombre_bufete.data.strip()
        b.direccion = form.direccion.data or None
        b.telefono = form.telefono.data or None
        b.email = form.email.data or None
        b.nit = form.nit.data or None
        b.pais = form.pais.data or None
        b.forma_contacto = form.forma_contacto.data or None
        b.facturacion_nombre = form.facturacion_nombre.data or None
        b.facturacion_nit = form.facturacion_nit.data or None
        b.facturacion_direccion = form.facturacion_direccion.data or None
        b.formas_pago = form.formas_pago.data or None
        b.metodo_pago_preferido = form.metodo_pago_preferido.data or None
        b.maneja_inventario_timbres_papel = bool(form.maneja_inventario_timbres_papel.data)
        b.incluye_libreria_plantillas_inicial = bool(form.incluye_libreria_plantillas_inicial.data)
        b.habilita_auditoria_borrado_logico = bool(form.habilita_auditoria_borrado_logico.data)
        b.habilita_dashboard_avanzado = bool(form.habilita_dashboard_avanzado.data)
        b.habilita_ayuda_contextual = bool(form.habilita_ayuda_contextual.data)
        b.habilita_papeleria_digital = bool(form.habilita_papeleria_digital.data)
        b.plan_id = form.plan_id.data
        db.session.commit()
        flash('Bufete actualizado', 'success')
        return redirect(url_for('superadmin.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='editar', bufete=b)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/eliminar', methods=['POST'])
@login_required
def eliminar_bufete(bufete_id):
    b = BufeteJuridico.query.get_or_404(bufete_id)
    b.activo = False
    db.session.commit()
    flash('Bufete desactivado', 'warning')
    return redirect(url_for('superadmin.listar_bufetes'))
