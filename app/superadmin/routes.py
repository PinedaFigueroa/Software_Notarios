# archivo: app/superadmin/routes.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:09
# motivo de la actualización: Dashboard global SuperAdmin con accesos CRUD
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import superadmin

@superadmin.route('/superadmin/dashboard')
@login_required
def dashboard_global():
    return render_template('superadmin/dashboard.html')
