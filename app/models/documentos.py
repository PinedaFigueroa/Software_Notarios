"" 
# archivo: app/models/documentos.py
# fecha de creación: 14 / 07 / 25 hora 21:15
# cantidad de lineas originales: 40 aprox.
# ultima actualización: 
# motivo de la actualizacion: 
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, String, Enum, Date, Time, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.models.enums import TipoDocumentoEnum, EstadoDocumentoEnum

class DocumentoNotarial(db.Model):
    __tablename__ = 'documentos_notariales'
    id = Column(Integer, primary_key=True)
    tipo_documento = Column(Enum(TipoDocumentoEnum), nullable=False)
    numero_instrumento = Column(Integer, nullable=False)  # para escrituras públicas
    fecha_otorgamiento = Column(Date, nullable=False)
    hora_otorgamiento = Column(Time, nullable=True)
    lugar_otorgamiento = Column(String(200), nullable=True)
    estado_documento = Column(Enum(EstadoDocumentoEnum), default=EstadoDocumentoEnum.BORRADOR, nullable=False)

    # Relaciones
    notario_id = Column(Integer, ForeignKey('notarios.id'))
    procurador_id = Column(Integer, ForeignKey('procuradores.id'))
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))

    notario = relationship('Notario')
    procurador = relationship('Procurador')
    bufete = relationship('BufeteJuridico')

    # Auditoría y borrado lógico
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<DocumentoNotarial id={self.id} tipo={self.tipo_documento}>"
