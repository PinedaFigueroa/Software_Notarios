# archivo: app/superadmin/__init__.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:18
# motivo de la actualización: Corregir nombre del Blueprint (superadmin_bp) con alias retrocompatible
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

# Blueprint oficial para registro en create_app
superadmin_bp = Blueprint('superadmin', __name__, template_folder='templates')

# Alias retrocompatible para que rutas existentes que importan 'superadmin' sigan funcionando
superadmin = superadmin_bp

# Importa vistas (mantiene side-effects de registro de rutas)
from . import routes, routes_bufetes, routes_usuarios  # noqa
