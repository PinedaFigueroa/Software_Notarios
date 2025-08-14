# archivo: app/superadmin/__init__.py
# fecha de creación: 2025-07-XX
# última actualización: 2025-08-13  | motivo: fijar import order + evitar circular imports
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint

# El nombre del blueprint será el prefijo de endpoints: superadmin.*
superadmin_bp = Blueprint(
    'superadmin',
    __name__,
    template_folder='templates'
)

# IMPORTAR RUTAS DESPUÉS de definir el blueprint (evita import circular)
from . import routes , routes_bufetes,   routes_usuarios        # 

try:
    from . import routes_planes  # 
except Exception:
    pass
