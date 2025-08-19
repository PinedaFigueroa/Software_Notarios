# app/lab/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import re

# --- Validadores de laboratorio (rápidos y prácticos) ---

# NIT (GT típico): permitimos "CF" (consumidor final), o dígitos con guión opcional.
# Ejemplos válidos: CF, 1234567-8, 12345678
NIT_REGEX = re.compile(r"^(?:CF|C/F|cf|c/f|[0-9]{3,12}(?:-[0-9])?)$")

def validate_nit(form, field):
    val = (field.data or "").strip()
    if not NIT_REGEX.match(val):
        raise ValidationError("NIT inválido (use dígitos, opcional guión y dígito verificador, o 'CF').")

# DPI (GT): 13 dígitos. Aceptamos espacios y guiones en la entrada y los ignoramos.
def validate_dpi(form, field):
    raw = (field.data or "")
    digits = re.sub(r"[^\d]", "", raw)
    if len(digits) != 13:
        raise ValidationError("DPI debe tener 13 dígitos.")
    if not digits.isdigit():
        raise ValidationError("DPI inválido.")
    # Si quisieras, aquí puedes añadir validación de depto/municipio según catálogo.

class NitDpiForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=120)])
    nit  = StringField("NIT",    validators=[DataRequired(), Length(min=2, max=32), validate_nit])
    dpi  = StringField("DPI",    validators=[DataRequired(), Length(min=6, max=32), validate_dpi])
    submit = SubmitField("Probar y guardar")
