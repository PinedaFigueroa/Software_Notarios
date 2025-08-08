# archivo: app/auth/__init__.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 4
# última actualización: 07 / 08 / 25 hora 20:40
# motivo de la actualización: Añadido docstring a la inicialización del blueprint de autenticación
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Inicializa el blueprint de autenticación para login/logout de usuarios.
"""

from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

from . import routes
