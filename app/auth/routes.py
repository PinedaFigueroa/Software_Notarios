# archivo: app/auth/routes.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 90
# última actualización: 09 / 08 / 25 hora 17:05
# motivo de la actualización: fix paréntesis faltante + limpieza de bloque innecesario
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas de autenticación: login y logout.
Redirige por rol:
- SUPERADMIN -> /superadmin/dashboard
- Otros      -> /dashboard
"""

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from . import auth_bp
from .forms import LoginForm
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data.strip()).first()
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            # si tu modelo no tiene UserMixin, añade get_id() o hereda UserMixin (recomendado)
            if hasattr(usuario, "is_active") and not usuario.is_active:
                flash('Tu usuario está inactivo. Contacta al administrador.', 'warning')
                return render_template('auth/login.html', form=form)
            login_user(usuario, remember=form.remember.data)
            if usuario.rol == RolUsuarioEnum.SUPERADMIN:
                return redirect(url_for('superadmin_bp.dashboard_global'))
            return redirect(url_for('dashboard.mostrar_dashboard'))
        flash('Credenciales incorrectas.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth_bp.login'))
