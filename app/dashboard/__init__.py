# archivo: app/dashboard/__init__.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 5
# última actualización: 31 / 07 / 25 hora 11:30
# motivo de la actualización: corrección de blueprint para rutas limpias
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes
