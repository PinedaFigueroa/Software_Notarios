# archivo: app/superadmin/routes_usuarios.py
# fecha de creación: 09 / 08 / 25
# última actualización: 09 / 08 / 25 hora 19:40
# motivo: stub mínimo para que no rompa el navbar ni las rutas
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

@superadmin_bp.route('/superadmin/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios_root():
    """Listado global de usuarios (stub)."""
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=[])

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios(bufete_id):
    """Listado de usuarios por bufete (stub)."""
    return render_template('superadmin/usuarios/listar_usuarios.html',
                           usuarios=[], bufete_id=bufete_id)
