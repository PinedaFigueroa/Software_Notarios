# archivo: app/superadmin/forms_usuarios.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 95
# última actualización: 09 / 08 / 25 hora 10:05
# motivo de la creación: Formularios WTForms para CRUD de Usuarios por bufete
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formularios para gestionar usuarios dentro de un bufete desde el SuperAdmin.
Incluye selección de rol y generación automática de username.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Optional, Length, Email

class UsuarioForm(FlaskForm):
    """Formulario para crear/editar usuarios de bufete."""
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    correo = StringField('Correo', validators=[Optional(), Email(), Length(max=150)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    rol = SelectField('Rol', validators=[DataRequired()], choices=[])
    password = PasswordField('Contraseña inicial (opcional)', validators=[Optional(), Length(min=4, max=128)])
    submit = SubmitField('Guardar')
