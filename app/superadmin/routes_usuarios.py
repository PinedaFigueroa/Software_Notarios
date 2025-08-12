# archivo: app/superadmin/routes_usuarios.py
# fecha de creación: 09 / 08 / 25
# cantidad de lineas originales: 26
# última actualización: 12 / 08 / 25 hora 01:24
# motivo de la actualización: Listado real de usuarios global y por bufete
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas de gestión de Usuarios para el panel del SuperAdmin.
Incluye:
- Listado global de usuarios
- Listado por bufete
(El CRUD completo se integrará a continuación, reutilizando forms_usuarios.py)
"""

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

# Modelos
from app.models.usuarios import Usuario

@superadmin_bp.route('/superadmin/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios_root():
    """Listado global de usuarios."""
    usuarios = Usuario.query.order_by(Usuario.id.asc()).all()
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios, bufete_id=None)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios(bufete_id):
    """Listado de usuarios por bufete."""
    usuarios = Usuario.query.filter(Usuario.bufete_id == bufete_id).order_by(Usuario.id.asc()).all()
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios, bufete_id=bufete_id)
