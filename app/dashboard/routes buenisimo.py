# archivo: app/dashboard/routes.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 10
# última actualización: 27 / 07 / 25 hora 21:15
# motivo de la creación: ruta principal para vista del dashboard
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from . import dashboard_bp

@dashboard_bp.route("/dashboard")
def mostrar_dashboard():
    return render_template("dashboard/dashboard.html", usuario="UsuarioEjemplo", rol="Notario")
