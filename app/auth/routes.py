# archivo: app/auth/routes.py
# fecha: 03 / 08 / 25
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from . import auth_bp
from app.models.usuarios import Usuario

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Usuario.query.filter_by(correo=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Bienvenido, login exitoso.", "success")
            return redirect(url_for("dashboard.mostrar_dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))
