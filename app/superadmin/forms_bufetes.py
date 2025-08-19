# archivo: app/superadmin/forms_bufetes.py
# fecha de creación: 2025-07-XX
# última actualización: 2025-08-13 | motivo: agregar plan_id + validación NIT opcional
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Email

plan_id = SelectField('Plan', coerce=int, choices=[], validators=[DataRequired()])

try:
    from app.validators.gt import validate_nit as _validate_nit
except Exception:
    _validate_nit = None

class BufeteForm(FlaskForm):
    nombre_bufete = StringField('Nombre del Bufete', validators=[DataRequired(), Length(max=255)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=150)])
    nit = StringField('NIT', validators=[Optional(), Length(max=50)])
    pais = StringField('País', validators=[Optional(), Length(max=50)])
    forma_contacto = StringField('Forma de Contacto', validators=[Optional(), Length(max=255)])

    facturacion_nombre = StringField('Facturación - Nombre', validators=[Optional(), Length(max=255)])
    facturacion_nit = StringField('Facturación - NIT', validators=[Optional(), Length(max=50)])
    facturacion_direccion = StringField('Facturación - Dirección', validators=[Optional(), Length(max=255)])

    formas_pago = StringField('Formas de pago (coma separadas)', validators=[Optional(), Length(max=150)])
    metodo_pago_preferido = StringField('Método de pago preferido', validators=[Optional(), Length(max=50)])

    maneja_inventario_timbres_papel = BooleanField('Inventario timbres/papel')
    incluye_libreria_plantillas_inicial = BooleanField('Librería de plantillas inicial')
    habilita_auditoria_borrado_logico = BooleanField('Auditoría y borrado lógico')
    habilita_dashboard_avanzado = BooleanField('Dashboard avanzado')
    habilita_ayuda_contextual = BooleanField('Ayuda contextual')
    habilita_papeleria_digital = BooleanField('Papelería digital')

    # ⬇️ Campo que faltaba para enlazar con Plan
    plan_id = SelectField('Plan', coerce=int, validators=[DataRequired()], choices=[])

    submit = SubmitField('Guardar')

    # Validaciones opcionales con librería GT
    def validate_nit(self, field):
        if _validate_nit and field.data:
            ok, msg = _validate_nit(field.data)
            if not ok:
                raise ValueError(msg or 'NIT inválido')

    def validate_facturacion_nit(self, field):
        if _validate_nit and field.data:
            ok, msg = _validate_nit(field.data)
            if not ok:
                raise ValueError(msg or 'NIT de facturación inválido')
