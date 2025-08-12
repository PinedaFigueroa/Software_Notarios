# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 09 / 08 / 25
# cantidad de lineas originales: 28
# última actualización: 12 / 08 / 25 hora 01:24
# motivo de la actualización: Listado real de bufetes + búsqueda + toggle activo (acciones)
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas de gestión de Bufetes para el panel del SuperAdmin.
Incluye:
- Listado con filtro por nombre (?q=...)
- Acción para activar/desactivar (toggle) vía POST
- Stubs para crear/editar conectados a las plantillas existentes
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

# Modelos y DB
from app.core_ext import db
from app.models.bufetes import BufeteJuridico

@superadmin_bp.route('/superadmin/bufetes')
@login_required
@rol_required(['SUPERADMIN'])
def listar_bufetes():
    """Listado de bufetes con búsqueda opcional por nombre_bufete."""
    q = request.args.get('q', type=str, default='')
    query = BufeteJuridico.query
    if q:
        # Búsqueda simple por coincidencia parcial (ilike)
        query = query.filter(BufeteJuridico.nombre_bufete.ilike(f"%{q}%"))
    bufetes = query.order_by(BufeteJuridico.id.asc()).all()
    return render_template('superadmin/bufetes/listar_bufetes.html', bufetes=bufetes, q=q)

@superadmin_bp.route('/superadmin/bufetes/nuevo', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def crear_bufete():
    """Formulario de creación de bufete.
    NOTA: Dejamos la creación real pendiente para alinear con forms_bufetes.py.
    """
    if request.method == 'POST':
        flash('Creación de bufete en construcción. Próximo paso: integrar WTForms y guardar en BD.', 'warning')
        return redirect(url_for('superadmin_bp.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', titulo='Crear Bufete (En construcción)')

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/editar', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def editar_bufete(bufete_id):
    """Editar un bufete existente (stub hasta integrar WTForms)."""
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    if request.method == 'POST':
        flash('Edición de bufete en construcción. Próximo paso: integrar WTForms y guardar cambios.', 'warning')
        return redirect(url_for('superadmin_bp.listar_bufetes'))
    return render_template('superadmin/bufetes/form_bufete.html', titulo=f'Editar: {bufete.nombre_bufete}', bufete=bufete)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/toggle', methods=['POST'])
@login_required
@rol_required(['SUPERADMIN'])
def toggle_estado_bufete(bufete_id):
    """Activa/Desactiva (borrado lógico) el bufete."""
    bufete = BufeteJuridico.query.get_or_404(bufete_id)
    bufete.activo = not bool(bufete.activo)
    db.session.add(bufete)
    db.session.commit()
    flash(f"Bufete '{bufete.nombre_bufete}' ahora está {'activo' if bufete.activo else 'inactivo'}.", 'success')
    # Mantener query string (por si el usuario estaba filtrando)
    next_url = url_for('superadmin_bp.listar_bufetes', q=request.args.get('q', ''))
    return redirect(next_url)
