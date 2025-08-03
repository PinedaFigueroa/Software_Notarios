# archivo: app/auth/__init__.py
# fecha: 03 / 08 / 25
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes
