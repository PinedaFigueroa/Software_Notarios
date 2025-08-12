# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 11 / 08 / 25
# cantidad de lineas originales: 120
# última actualización: 12 / 08 / 25 hora 03:25
# motivo de la actualización: WTForms Bufetes (crear/editar) con selección de plan y activo
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""Formularios WTForms para la gestión de Bufetes."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

def get_plan_choices():
    plans = [("", "-- Sin plan --")]
    try:
        from app.models.plan import Plan
    except Exception:
        try:
            from app.models.planes import Plan  # fallback
        except Exception:
            Plan = None
    if 'Plan' in locals() and Plan is not None:
        try:
            plans += [(str(p.id), p.nombre) for p in Plan.query.order_by(Plan.nombre.asc()).all()]
        except Exception:
            pass
    return plans

class BufeteForm(FlaskForm):
    nombre_bufete = StringField(
        "Nombre del bufete",
        validators=[DataRequired(), Length(min=2, max=150)],
        render_kw={"placeholder": "Ej. Notaría X", "title": "Nombre comercial del bufete"}
    )
    plan_id = SelectField("Plan", choices=[], default="", render_kw={"title": "Plan de suscripción asociado (opcional)"})
    activo = BooleanField("Activo", default=True, render_kw={"title": "Indica si el bufete está habilitado"})
    submit = SubmitField("Guardar")

    def refresh_choices(self):
        self.plan_id.choices = get_plan_choices()
