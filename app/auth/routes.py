# archivo: app/auth/routes.py
# última actualización: 14/08/25 — reemplaza werkzeug.urls.url_parse por urllib.parse.urlparse
# -*- coding: utf-8 -*-

"""
Rutas de autenticación: login y logout.
Redirige por rol:
- SUPERADMIN -> superadmin.dashboard_global (fallback: superadmin.dashboard)
- Otros      -> dashboard.mostrar_dashboard (fallbacks: dashboard.index, dashboard.dashboard, /)
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from urllib.parse import urlparse  # ✅ reemplazo compatible

from . import auth_bp
from .forms import LoginForm
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum


def _redirect_superadmin():
    for ep in ("superadmin.dashboard_global", "superadmin.dashboard"):
        try:
            return redirect(url_for(ep))
        except Exception:
            continue
    return redirect("/dashboard")


def _redirect_usuario():
    for ep in ("dashboard.mostrar_dashboard", "dashboard.index", "dashboard.dashboard"):
        try:
            return redirect(url_for(ep))
        except Exception:
            continue
    return redirect("/")


def _safe_next_url(next_url: str | None):
    """Solo permite rutas internas relativas (p. ej. '/dashboard')."""
    if not next_url:
        return None
    p = urlparse(next_url)
    # Sin esquema, sin host, y empieza con '/'
    if not p.scheme and not p.netloc and next_url.startswith("/"):
        return next_url
    return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya hay sesión, redirige por rol
    if current_user.is_authenticated:
        return _redirect_superadmin() if getattr(current_user, "rol", None) == RolUsuarioEnum.SUPERADMIN else _redirect_usuario()

    form = LoginForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip()
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            if hasattr(usuario, "is_active") and not usuario.is_active:
                flash("Tu usuario está inactivo. Contacta al administrador.", "warning")
                return render_template("auth/login.html", form=form)

            remember_flag = bool(getattr(getattr(form, "remember", None), "data", False))
            login_user(usuario, remember=remember_flag)

            next_url = _safe_next_url(request.args.get("next"))
            if next_url:
                return redirect(next_url)

            return _redirect_superadmin() if usuario.rol == RolUsuarioEnum.SUPERADMIN else _redirect_usuario()

        flash("Credenciales incorrectas.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))
