# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:09
# motivo de la actualización: CRUD Bufetes alineado a BufeteJuridico y borrado lógico en activo
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import superadmin
from .forms_bufetes import BufeteForm

# db import robusto
try:
    from app.models.core import db
except Exception:
    try:
        from app.core_ext import db
    except Exception:
        db = None

try:
    from app.models.bufetes import BufeteJuridico
except Exception:
    BufeteJuridico = None

@superadmin.route('/superadmin/bufetes')
@login_required
def listar_bufetes():
    bufetes = BufeteJuridico.query.filter_by(activo=True).all() if BufeteJuridico else []
    return render_template('superadmin/bufetes/listar_bufetes.html', bufetes=bufetes)

@superadmin.route('/superadmin/bufetes/nuevo', methods=['GET', 'POST'])
@login_required
def crear_bufete():
    form = BufeteForm()
    if form.validate_on_submit() and BufeteJuridico and db:
        if BufeteJuridico.query.filter_by(nombre_bufete=form.nombre_bufete.data).first():
            flash('Ya existe un bufete con ese nombre.', 'warning')
            return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='crear')
        b = BufeteJuridico(nombre_bufete=form.nombre_bufete.data, activo=True)
        db.session.add(b)
        db.session.commit()
        flash('Bufete creado', 'success')
        return redirect(url_for('superadmin.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='crear')

@superadmin.route('/superadmin/bufetes/<int:bufete_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_bufete(bufete_id):
    if not (BufeteJuridico and db):
        return redirect(url_for('superadmin.listar_bufetes'))
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    form = BufeteForm(obj=bufete)
    if form.validate_on_submit():
        existe = BufeteJuridico.query.filter(BufeteJuridico.id != bufete.id, BufeteJuridico.nombre_bufete == form.nombre_bufete.data).first()
        if existe:
            flash('Ese nombre ya está en uso por otro bufete.', 'warning')
            return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='editar', bufete=bufete)
        bufete.nombre_bufete = form.nombre_bufete.data
        db.session.commit()
        flash('Bufete actualizado', 'success')
        return redirect(url_for('superadmin.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', form=form, modo='editar', bufete=bufete)

@superadmin.route('/superadmin/bufetes/<int:bufete_id>/eliminar', methods=['POST'])
@login_required
def eliminar_bufete(bufete_id):
    if not (BufeteJuridico and db):
        return redirect(url_for('superadmin.listar_bufetes'))
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    bufete.activo = False  # borrado lógico
    db.session.commit()
    flash('Bufete eliminado (lógico)', 'warning')
    return redirect(url_for('superadmin.listar_bufetes'))
