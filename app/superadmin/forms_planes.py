# archivo: app/superadmin/forms_planes.py
# última actualización: 13/08/25 hora 02:39
# autor: Giancarlo + Tars-90
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class PlanForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=255)])
    max_notarios = IntegerField('Max Notarios', validators=[DataRequired(), NumberRange(min=0)])
    max_procuradores = IntegerField('Max Procuradores', validators=[DataRequired(), NumberRange(min=0)])
    max_asistentes = IntegerField('Max Asistentes', validators=[DataRequired(), NumberRange(min=0)])
    max_documentos = IntegerField('Max Documentos', validators=[DataRequired(), NumberRange(min=0)])
    storage_mb = IntegerField('Almacenamiento (MB)', validators=[DataRequired(), NumberRange(min=0)])
    precio_mensual = DecimalField('Precio Mensual (Q)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    es_personalizado = BooleanField('Es personalizado')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')
