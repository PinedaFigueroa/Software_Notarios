# archivo: app/models/bufetes.py
# fecha de creación: 15 / 07 / 25 hora 09:20
# cantidad de lineas originales: ~40
# ultima actualización:
# motivo de la actualización: modelo principal de bufetes
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Modelo BufeteJuridico:
Representa un bufete con configuración, datos de contacto y feature flags.
"""

from app.extensions import db
from sqlalchemy.orm import relationship

class BufeteJuridico(db.Model):
    __tablename__ = 'bufetes_juridicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    nit = db.Column(db.String(20))
    correo = db.Column(db.String(255))
    forma_contacto = db.Column(db.String(100))

    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
    plan = relationship("Plan", back_populates="bufetes")
    movimientos = db.relationship('MovimientoCuenta', back_populates='bufete', cascade='all, delete-orphan')


    # Feature flags
    usa_control_inventario = db.Column(db.Boolean, default=False)
    usa_auditoria = db.Column(db.Boolean, default=False)
    usa_digital = db.Column(db.Boolean, default=False) # protocolo, timbres digitales

    usuarios = relationship("Usuario", back_populates="bufete")

    def __repr__(self):
        return f"<BufeteJuridico nombre={self.nombre}>"
