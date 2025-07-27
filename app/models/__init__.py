# archivo: app/models/__init__.py
# fecha de creación: 15 / 07 / 25 hora 09:15
# cantidad de lineas originales: ~10
# ultima actualización:
# motivo de la actualización: inicialización del módulo models
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Inicializa el paquete models e importa todas las clases
para que SQLAlchemy y Flask las reconozcan.
"""

from .planes import Plan
from .relaciones import NotarioProcurador
from .pagos import PagoBufete
from .cuenta_corriente import MovimientoCuenta
from .usuarios import Usuario
from .documentos import DocumentoNotarial
# from .clausulas_puntos import ClausulaPunto
from .enums import (
    FormaPagoEnum,
    EstadoDocumentoEnum,
    RolUsuarioEnum,
    EstadoUsuarioEnum,
    TipoClausulaEnum,
    TipoDocumentoEnum,
    TipoBienEnum,
)

# Si tienes más modelos (ejemplo: relaciones, auditoria, librería, etc.)
# los importas aquí igualmente para que los detecte Flask-Migrate
