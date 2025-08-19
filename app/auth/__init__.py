# archivo: app/auth/__init__.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 15
# última actualización: 09 / 08 / 25 hora 16:10
# motivo de la creación: Inicialización del blueprint de autenticación
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""Inicializa el blueprint de autenticación (login/logout)."""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates') #decia auth_bp

from . import routes  
