# archivo: app/superadmin/routes.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 60
# última actualización: 09 / 08 / 25 hora 16:55
# motivo: Dashboard global para SuperAdmin
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas principales del área SuperAdmin.
Incluye el dashboard global con métricas generales:
- Total de bufetes
- Total de usuarios
- Total de superadmins
- Espacio usado (placeholder)
"""

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

# Modelos para métricas
from app.models.bufetes import BufeteJuridico
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum


@superadmin_bp.route("/superadmin/dashboard")
@login_required
@rol_required(["SUPERADMIN"])
def dashboard_global():
    total_bufetes = BufeteJuridico.query.count()
    total_usuarios = Usuario.query.count()
    total_superadmins = Usuario.query.filter(Usuario.rol == RolUsuarioEnum.SUPERADMIN).count()
    espacio_usado = "45 MB"
    return render_template("superadmin/dashboard.html",
                           total_bufetes=total_bufetes,
                           total_usuarios=total_usuarios,
                           total_superadmins=total_superadmins,
                           espacio_usado=espacio_usado)