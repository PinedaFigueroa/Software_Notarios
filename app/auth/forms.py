# archivo: app/auth/forms.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 35
# última actualización: 09 / 08 / 25 hora 16:10
# motivo de la creación: Formulario de login para autenticación
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formulario de login para autenticación de usuarios.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """Formulario de ingreso con username y password."""
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=3, max=128)])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')
