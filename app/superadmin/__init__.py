# archivo: app/superadmin/__init__.py
# fecha de creación: 07 / 08 / 25
# última actualización: 09 / 08 / 25 hora 10:05
# motivo: registrar blueprints y rutas del superadmin
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""Inicialización del blueprint SuperAdmin y registro de sus rutas."""

from flask import Blueprint

superadmin_bp = Blueprint('superadmin_bp', __name__, template_folder='templates')

from . import routes            # dashboard_global existente
from . import routes_bufetes    # CRUD bufetes
from . import routes_usuarios   # CRUD usuarios
