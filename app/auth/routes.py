# archivo: app/auth/routes.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 25
# última actualización: 07 / 08 / 25 hora 20:40
# motivo de la actualización: Corrección de login para usar password_hash y control de errores
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Rutas de autenticación para login y logout de usuarios del sistema.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models.usuarios import Usuario
from .forms import LoginForm
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            login_user(usuario)
            flash('Sesión iniciada correctamente.', 'success')
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
