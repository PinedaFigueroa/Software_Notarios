# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 09 / 08 / 25
# cantidad de líneas originales: 70
# última actualización: 09 / 08 / 25 hora 10:05
# motivo de la creación: Formularios WTForms para CRUD de Bufetes
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formularios para crear y editar bufetes jurídicos.
Incluye selección de Plan y campos básicos de contacto.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Email

class BufeteForm(FlaskForm):
    """Formulario de creación/edición de bufetes."""
    nombre_bufete = StringField('Nombre del Bufete', validators=[DataRequired(), Length(max=255)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=150)])
    nit = StringField('NIT', validators=[Optional(), Length(max=50)])
    pais = StringField('País', validators=[Optional(), Length(max=50)])
    plan_id = SelectField('Plan', coerce=int, validators=[DataRequired()])
    activo = BooleanField('Activo', default=True)

    submit = SubmitField('Guardar')
