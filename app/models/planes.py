# archivo: app/models/planes.py
# fecha de creación: 14 / 07 / 25 hora 23:50
# cantidad de lineas originales: 30 aprox.
# última actualización:
# motivo de la actualización:
# lineas actuales: ____
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app import db

class Plan(db.Model):
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(250), nullable=True)
    max_notarios = Column(Integer, default=1)
    max_procuradores = Column(Integer, default=1)
    max_asistentes = Column(Integer, default=1)
    max_escrituras_mensuales = Column(Integer, default=10)
    max_actas_mensuales = Column(Integer, default=10)
    max_storage_mb = Column(Integer, default=500)
    activo = Column(Boolean, default=True)

    # Relación inversa: bufetes que tienen este plan
    bufetes = relationship('BufeteJuridico', back_populates='plan')

    def __repr__(self):
        return f"<Plan(id={self.id}, nombre='{self.nombre}')>"
