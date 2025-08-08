
# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 08 / 08 / 25
# cantidad de líneas originales: 20
# última actualización: 08 / 08 / 25 hora 11:20
# motivo de la creación: Formulario para crear/editar bufetes
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class BufeteForm(FlaskForm):
    nombre_bufete = StringField('Nombre del Bufete', validators=[DataRequired(), Length(max=150)])
    responsable = StringField('Responsable', validators=[Optional(), Length(max=100)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    correo = StringField('Correo', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Guardar')
