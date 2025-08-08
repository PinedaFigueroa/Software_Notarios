# archivo: app/models/planes.py
# fecha de creación: 16/07/25 hora 09:50
# cantidad de lineas originales: ~40
# última actualización: 26/07/25 hora 20:10
# motivo de la actualización: corrección de importación, expansión del modelo y preparación para planes base
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

# importación centralizada
from app.core_ext import db
from app.models.core import *
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

class Plan(db.Model):
    """
    Modelo: Plan

    Representa un plan contratado por un bufete jurídico.

    Campos principales:
    - nombre: Nombre del plan (ej. Demo, Profesional, Ilimitado)
    - descripcion: Breve descripción visible en el dashboard
    - límites: usuarios, documentos, almacenamiento
    - precio_mensual: Costo en quetzales
    - es_personalizado: Bandera para planes fuera del catálogo general
    - activo: Si está disponible para nuevos bufetes
    - fechas: creación y actualización

    Usos:
    - Control de acceso según el plan contratado
    - Facturación y visualización de plan actual
    """
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    max_notarios = Column(Integer, nullable=False, default=1)
    max_procuradores = Column(Integer, nullable=False, default=1)
    max_asistentes = Column(Integer, nullable=False, default=0)
    max_documentos = Column(Integer, nullable=False, default=10)
    storage_mb = Column(Integer, nullable=False, default=100)

    precio_mensual = Column(Float, nullable=False, default=0.0)
    es_personalizado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

    # Auditoría
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    bufetes = relationship("BufeteJuridico", back_populates="plan")

    def es_valido_para(self, notarios, procuradores, asistentes, documentos, uso_mb):
        return (
            notarios <= self.max_notarios and
            procuradores <= self.max_procuradores and
            asistentes <= self.max_asistentes and
            documentos <= self.max_documentos and
            uso_mb <= self.storage_mb
        )

    def __repr__(self):
        return f"<Plan {self.nombre} Q{self.precio_mensual}>"
