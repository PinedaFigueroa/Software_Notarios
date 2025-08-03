# archivo: app/auth/routes.py
# fecha de creación: 03 / 08 / 25
# cantidad de líneas originales: 50 aprox.
# última actualización: 03 / 08 / 25 hora 20:30
# motivo de la actualización: implementación inicial de login y logout
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuarios import Usuario
from app.extensions import db, login_manager
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.mostrar_dashboard'))
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard.mostrar_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))
