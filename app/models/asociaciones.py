# archivo: app/models/asociaciones.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 50
# última actualización: 27 / 07 / 25 hora 20:35
# motivo de la creación: modelar relación muchos-a-muchos entre notarios y procuradores
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class NotarioProcuradorAsociacion(db.Model):
    __tablename__ = "notario_procurador_asociacion"

    id = Column(Integer, primary_key=True)
    notario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    procurador_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'), nullable=False)

    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_reasignacion = Column(DateTime, nullable=True)
    motivo_reasignacion = Column(String(255), nullable=True)

    activo = Column(Boolean, default=True)

    # Relaciones explícitas
    notario = relationship("Usuario", foreign_keys=[notario_id])
    procurador = relationship("Usuario", foreign_keys=[procurador_id])
    bufete = relationship("BufeteJuridico")

    def __repr__(self):
        return f"<Asociación Notario:{self.notario_id} ↔ Procurador:{self.procurador_id}>"
