# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 09 / 08 / 25
# última actualización: 09 / 08 / 25 hora 20:20
# motivo: stubs mínimos para no romper navegación (listar y crear)
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

@superadmin_bp.route('/superadmin/bufetes')
@login_required
@rol_required(['SUPERADMIN'])
def listar_bufetes():
    """Listado de bufetes (stub)."""
    # TODO: reemplazar por consulta real a BufeteJuridico.query.all()
    bufetes = []
    return render_template('superadmin/bufetes/listar_bufetes.html', bufetes=bufetes)

@superadmin_bp.route('/superadmin/bufetes/nuevo', methods=['GET'])
@login_required
@rol_required(['SUPERADMIN'])
def crear_bufete():
    """Formulario de creación de bufete (stub)."""
    # TODO: implementar WTForm real y guardado en BD
    return render_template('superadmin/bufetes/form_bufete.html', titulo='Crear Bufete (En construcción)')
