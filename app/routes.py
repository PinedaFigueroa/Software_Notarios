# archivo: app/routes.py
# fecha de actualización: 29 / 07 / 25
# motivo: mostrar métricas reales en dashboard con cards Bootstrap
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

# app/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # home simple: si hay sesión manda al dashboard, si no al login
    try:
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.mostrar_dashboard"))
    except Exception:
        pass
    try:
        return redirect(url_for("auth.login"))
    except Exception:
        return "OK", 200  # fallback sin romper
        

@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200
