# archivo: app/utils/roles_required.py
# fecha de creación: 07 / 08 / 25
# cantidad de lineas originales: 15
# última actualización: 08 / 08 / 25 hora 13:20
# motivo de la actualización: Comparación correcta de Enum con string
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Decorador para restringir acceso a rutas según los roles definidos en RolUsuarioEnum.
"""

from functools import wraps
from flask import abort
from flask_login import current_user

def rol_required(roles):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if current_user.rol.name not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_view
    return wrapper
