# archivo: app/superadmin/routes_bufetes.py
# fecha de creación: 08 / 08 / 25
# cantidad de líneas originales: 18
# última actualización: 08 / 08 / 25 hora 13:55
# motivo de la actualización: Corrección de importación de decorador y docstrings
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas del módulo superadmin para listar bufetes.
"""

from flask import render_template
from flask_login import login_required
from app.utils.roles_required import rol_required
from app.models.bufetes import BufeteJuridico
from . import superadmin_bp

@superadmin_bp.route("/superadmin/bufetes")
@login_required
@rol_required(["SUPERADMIN"])
def lista_bufetes():
    """
    Muestra la lista de bufetes registrados para el superadmin.
    """
    bufetes = BufeteJuridico.query.all()
    return render_template("superadmin/lista_bufetes.html", bufetes=bufetes)
