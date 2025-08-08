# archivo: app/auth/routes.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 25
# última actualización: 08 / 08 / 25 hora 13:06
# motivo de la actualización: agregar dashboards por usuario
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas de autenticación para login y logout de usuarios del sistema.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum
from .forms import LoginForm
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            login_user(usuario)
            flash("Sesión iniciada exitosamente 080825", "success")
            # Redireccionar según rol
            if usuario.rol == RolUsuarioEnum.SUPERADMIN:
                return redirect(url_for("superadmin_bp.dashboard_global"))
            elif usuario.rol == RolUsuarioEnum.NOTARIO:
                return redirect(url_for("dashboard_bp.dashboard_notario"))
            elif usuario.rol == RolUsuarioEnum.ADMINISTRADOR:
                return redirect(url_for("dashboard_bp.dashboard_admin"))
            elif usuario.rol == RolUsuarioEnum.PROCURADOR:
                return redirect(url_for("dashboard_bp.dashboard_procurador"))
            elif usuario.rol == RolUsuarioEnum.ASISTENTE:
                return redirect(url_for("dashboard_bp.dashboard_asistente"))
            else:
                return redirect(url_for("dashboard_bp.dashboard_default"))
                # return redirect(url_for('dashboard_bp.dashboard'))
                return redirect(url_for('dashboard.mostrar_dashboard'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth_bp.login'))
