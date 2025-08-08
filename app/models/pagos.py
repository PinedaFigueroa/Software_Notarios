# archivo: app/models/pagos.py
# fecha de creación: 16/07/25 hora 09:52
# cantidad de lineas originales: ~30
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-


#from app.models.core import db
from app.core_ext import db
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
from app.models.enums import FormaPagoEnum

class PagoBufete(db.Model):
    """
    Registra cada pago realizado por un bufete.
    """
    __tablename__ = 'pagos_bufete'

    id = Column(Integer, primary_key=True)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    monto_pagado = Column(Float, nullable=False)
    fecha_pago = Column(Date, default=datetime.date.today)
    forma_pago = Column(Enum(FormaPagoEnum), nullable=False)
    detalle = Column(String(250), nullable=True)  # Ej: "Depósito No 123, Banco X"

    bufete = relationship('BufeteJuridico')

    def __repr__(self):
        return f"<Pago {self.id} Bufete:{self.bufete_id} Q{self.monto_pagado}>"
