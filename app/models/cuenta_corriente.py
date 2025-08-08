# archivo: app/models/cuenta_corriente.py
# fecha de creación: 16/07/25 hora 09:54
# cantidad de lineas originales: ~25
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-


#from app.models.core import db
from app.core_ext import db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
import datetime  # <<<< ESTE IMPORT ES CLAVE

class MovimientoCuenta(db.Model):
    """
    Movimientos de la cuenta corriente del bufete:
    - cargos
    - pagos
    - ajustes
    """
    __tablename__ = 'cuenta_corriente'

    id = Column(Integer, primary_key=True)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    fecha = Column(Date, default=datetime.date.today)
    descripcion = Column(String(200), nullable=False)
    monto = Column(Float, nullable=False)  # +cargos, -pagos

    def __repr__(self):
        return f"<Movimiento {self.id} Bufete:{self.bufete_id} Q{self.monto}>"
