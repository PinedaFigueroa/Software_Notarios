# -*- coding: utf-8 -*-
# archivo: app/models/planes.py
# autor: Giancarlo + Tars-90
# última actualización: 25 / 07 / 25
# Descripción: Modelo de Planes para definir límites y características contratadas por cada bufete

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app import db

class Plan(db.Model):
    """
    Modelo que define los planes de suscripción del sistema.
    Permite controlar límites como usuarios, documentos, almacenamiento, etc.
    """
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(250), nullable=True)

    # Límites
    max_notarios = Column(Integer, default=1)
    max_procuradores = Column(Integer, default=1)
    max_asistentes = Column(Integer, default=1)
    max_escrituras_mensuales = Column(Integer, default=10)
    max_actas_mensuales = Column(Integer, default=10)
    max_storage_mb = Column(Integer, default=500)

    activo = Column(Boolean, default=True)

    # Relación inversa: bufetes que usan este plan
    bufetes = relationship('BufeteJuridico', back_populates='plan')

    def __repr__(self):
        return f"<Plan(id={self.id}, nombre='{self.nombre}')>"
