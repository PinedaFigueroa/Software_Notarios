# archivo: app/models/core.py
# fecha de creación: 06 / 08 / 25
# cantidad de líneas originales: 15
# última actualización: 06 / 08 / 25 hora 18:32
# motivo de la creación: Centralización de imports y definiciones comunes para modelos
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, backref
import datetime

# Alias útiles
utcnow = datetime.datetime.utcnow
