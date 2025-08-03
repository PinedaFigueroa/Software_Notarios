# archivo: app/dashboard/routes.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 10
# última actualización: 03 / 08 / 25 hora 21:50
# motivo de la actualización: corregir URL del dashboard y proteger con login
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from . import dashboard_bp
from flask_login import login_required, current_user

@dashboard_bp.route("/")  # Ahora la ruta será /dashboard
@login_required
def mostrar_dashboard():
    """
    Muestra la vista principal del dashboard del bufete.
    Solo accesible si el usuario ha iniciado sesión.
    """
    return render_template(
        "dashboard/dashboard.html",
        usuario=current_user.nombre_completo if current_user.is_authenticated else "Usuario",
        rol=getattr(current_user, "rol", "Desconocido")
    )
