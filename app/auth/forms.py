# archivo: app/auth/forms.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 15
# última actualización: 07 / 08 / 25 hora 20:40
# motivo de la actualización: Corrección de import y validación para login
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formulario de login de usuario para autenticación en el sistema.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
