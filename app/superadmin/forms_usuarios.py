# archivo: app/superadmin/forms_usuarios.py
# fecha de creación: 11 / 08 / 25
# cantidad de lineas originales: 160
# última actualización: 12 / 08 / 25 hora 01:32
# motivo de la actualización: Crear WTForm para Usuarios (crear/editar) con rol y bufete
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Formularios WTForms para la gestión de Usuarios desde SuperAdmin.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

def get_bufete_choices():
    bufetes = []
    BufeteJuridico = None
    try:
        from app.models.usuarios import BufeteJuridico  # opción 1
    except Exception:
        try:
            from app.models.bufetes import BufeteJuridico  # opción 2
        except Exception:
            BufeteJuridico = None
    if BufeteJuridico is not None:
        try:
            bufetes = [(str(b.id), b.nombre_bufete) for b in BufeteJuridico.query.order_by(BufeteJuridico.nombre_bufete.asc()).all()]
        except Exception:
            bufetes = []
    return bufetes

def get_role_choices():
    # Intentamos leer Enum desde el modelo
    choices = []
    try:
        from app.models.usuarios import RolUsuarioEnum
        # Generar pares (name, label) legibles
        for r in RolUsuarioEnum:
            choices.append((r.name, r.name.title().replace("_", " ")))
    except Exception:
        # fallback común
        choices = [
            ("SUPERADMIN", "Superadmin"),
            ("ADMINISTRADOR", "Administrador"),
            ("NOTARIO", "Notario"),
            ("PROCURADOR", "Procurador"),
            ("ASISTENTE", "Asistente"),
        ]
    return choices

class UsuarioForm(FlaskForm):
    nombres = StringField("Nombres", validators=[DataRequired(), Length(min=1, max=100)])
    apellidos = StringField("Apellidos", validators=[Optional(), Length(max=120)])
    correo = StringField("Correo", validators=[Optional(), Email(), Length(max=150)])
    rol = SelectField("Rol", choices=[], validators=[DataRequired()])
    bufete_id = SelectField("Bufete", choices=[], validators=[Optional()])
    activo = BooleanField("Activo", default=True)
    submit = SubmitField("Guardar")

    def refresh_choices(self):
        self.rol.choices = get_role_choices()
        self.bufete_id.choices = [("", "-- Sin asignar --")] + get_bufete_choices()
