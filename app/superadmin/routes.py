# archivo: app/superadmin/routes.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 36
# última actualización: 07 / 08 / 25 hora 18:15
# motivo de la creación: dashboard global para superadmin
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp
from app.models.usuarios import Usuario
from app.models.bufetes import BufeteJuridico

@superadmin_bp.route("/superadmin/dashboard")
@login_required
@rol_required(["SUPERADMIN"])
def dashboard_global():
    total_bufetes = BufeteJuridico.query.count()
    total_usuarios = Usuario.query.count()
    total_superadmins = Usuario.query.filter_by(rol="SUPERADMIN").count()

    # Espacio usado: futuro (placeholder)
    espacio_usado = "45 MB"

    return render_template(
        "superadmin/dashboard.html",
        total_bufetes=total_bufetes,
        total_usuarios=total_usuarios,
        total_superadmins=total_superadmins,
        espacio_usado=espacio_usado
    )
