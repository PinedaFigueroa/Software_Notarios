# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 11 / 08 / 25
# cantidad de lineas originales: 120
# última actualización: 12 / 08 / 25 hora 01:32
# motivo de la actualización: Crear WTForm para Bufetes (crear/editar) con selección de plan y activo
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formularios WTForms para la gestión de Bufetes.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

# Cargamos Plan dinámicamente para choices
def get_plan_choices():
    plans = []
    try:
        from app.models.plan import Plan  # opción 1
    except Exception:
        try:
            from app.models.planes import Plan  # opción 2
        except Exception:
            Plan = None
    if 'Plan' in locals() and Plan is not None:
        try:
            plans = [(str(p.id), p.nombre) for p in Plan.query.order_by(Plan.nombre.asc()).all()]
        except Exception:
            plans = []
    # Agregar opción vacía al inicio
    return [("", "-- Sin plan --")] + plans

class BufeteForm(FlaskForm):
    nombre_bufete = StringField("Nombre del bufete", validators=[DataRequired(), Length(min=2, max=150)])
    plan_id = SelectField("Plan", choices=[], default="")
    activo = BooleanField("Activo", default=True)
    submit = SubmitField("Guardar")

    def refresh_choices(self):
        self.plan_id.choices = get_plan_choices()
