# archivo: app/superadmin/__init__.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 4
# última actualización: 07 / 08 / 25 hora 18:15
# motivo de la creación: inicialización del blueprint de superadmin
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

superadmin_bp = Blueprint('superadmin_bp', __name__, template_folder='templates')

from . import routes, routes_bufetes, routes_extra
