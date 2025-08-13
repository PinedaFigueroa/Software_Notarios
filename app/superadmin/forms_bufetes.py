# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:09
# motivo de la actualización: Form de BufeteJuridico usando nombre_bufete
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BufeteForm(FlaskForm):
    nombre_bufete = StringField('Nombre del Bufete', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Guardar')
