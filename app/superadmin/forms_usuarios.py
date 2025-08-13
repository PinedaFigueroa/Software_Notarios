# archivo: app/superadmin/forms_usuarios.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:09
# motivo de la actualización: Form de Usuario con enums y hash de password
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class UsuarioForm(FlaskForm):
    username = StringField('Usuario (único)', validators=[DataRequired(), Length(max=150)])
    correo = StringField('Correo', validators=[Optional(), Length(max=150)])
    password = PasswordField('Contraseña (dejar vacío para no cambiar)', validators=[Optional(), Length(max=255)])
    rol = SelectField('Rol', validators=[DataRequired()], choices=[])
    bufete_id = SelectField('Bufete', coerce=int, validators=[DataRequired()], choices=[])
    submit = SubmitField('Guardar')
