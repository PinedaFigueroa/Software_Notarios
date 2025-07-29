# archivo: app/dashboard/__init__.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 5
# última actualización: 27 / 07 / 25 hora 21:15
# motivo de la creación: iniciar blueprint del dashboard
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

from . import routes
