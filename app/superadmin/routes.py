# archivo: app/superadmin/routes.py
# fecha de creación: 2025-07-XX
# última actualización: 2025-08-13 | motivo: usar superadmin_bp (no 'superadmin') para evitar circular import
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import superadmin_bp  # ✅ importar el blueprint ya definido en __init__.py

@superadmin_bp.route('/superadmin/dashboard')
@login_required
def dashboard_global():
    """Panel del SuperAdmin."""
    return render_template('superadmin/dashboard.html')
