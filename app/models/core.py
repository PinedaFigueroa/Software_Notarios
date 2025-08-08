# archivo: app/models/core.py
# fecha de creación: 06 / 08 / 25
# cantidad de líneas originales: 30 aprox.
# última actualización: 07 / 08 / 25 hora 19:15
# motivo de la actualización: Incluir todos los tipos comunes para modelos SQLAlchemy
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Core para modelos: centraliza todos los tipos y funciones de SQLAlchemy
para evitar imports repetidos y errores por omisión.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, Float, Text, Enum, 
    ForeignKey, Time, LargeBinary, Numeric, JSON
)
from sqlalchemy.orm import relationship, backref
import datetime

# Atajo útil para timestamps
utcnow = datetime.datetime.utcnow
