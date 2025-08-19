# archivo: app/models/usuarios.py
# fecha de creación: 26 / 07 / 25
# cantidad de lineas originales: 123
# última actualización: 27 / 07 / 25 hora 00:46
# motivo de la actualización: Consolidación total de modelos de usuario y bufetes, con soporte multitenancy
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Este módulo define el modelo principal de usuarios del sistema notarial multitenant.

Incluye:
- Usuario (abstracto): Base para todos los usuarios.
- Notario: Extiende Usuario, con datos colegiado y firma electrónica.
- Procurador: Extiende Usuario, usado para redacción.
- Asistente: Extiende Usuario, tareas complementarias.

Estos modelos soportan:
- Multitenancy por bufete
- Borrado lógico para auditoría
- Adaptabilidad para exportación a otros países
"""

# archivo: app/models/usuarios.py
# Consolidado por Tars-90 el 26/07/2025
# Contiene los modelos completos de Usuario, Notario, Procurador, Asistente y BufeteJuridico

#import datetime
#from app import db
#from sqlalchemy.orm import relationship
# from sqlalchemy import Enum, Boolean, DateTime, ForeignKey

from app.models.core import * 
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum
from flask_login import UserMixin


# ------------------------
# MODELO: Usuario base
# ------------------------
class Usuario(UserMixin,db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    correo = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(Enum(RolUsuarioEnum), nullable=False)
    estado = db.Column(Enum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO)

    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion_laboral = db.Column(db.String(255), nullable=True)
    preferencia_contacto_red_social = db.Column(db.String(100), nullable=True)

    bufete_id = db.Column(db.Integer, db.ForeignKey('bufetes_juridicos.id'))
    bufete = relationship("BufeteJuridico", back_populates="usuarios")

    # Auditoría y control
    borrado_logico = db.Column(Boolean, default=False)

 # ---- Flask-Login integration ----
    @property
    def is_active(self) -> bool:
        """Requerido por Flask-Login: usuario activo si estado=ACTIVO y no borrado lógicamente."""
        # Activo si estado = ACTIVO y no está borrado lógicamente
        from app.models.enums import EstadoUsuarioEnum
        return (self.estado == EstadoUsuarioEnum.ACTIVO) and (not self.borrado_logico)

    # UserMixin ya implementa: is_authenticated, is_anonymous, get_id()

    def __repr__(self):
        return "<Usuario %s (%s)>" % (self.username, self.rol)

# ------------------------
# MODELO: Notario
# ------------------------
class Notario(Usuario):
    __tablename__ = 'notarios'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    numero_colegiado = db.Column(db.String(20), nullable=False)
    colegiado_activo = db.Column(Boolean, default=True, nullable=False)
    fecha_verificacion = db.Column(db.DateTime, nullable=True)

    firma_electronica_registrada = db.Column(Boolean, default=False)
    proveedor_firma_electronica = db.Column(db.String(100), nullable=True)

# ------------------------
# MODELO: Procurador
# ------------------------
class Procurador(Usuario):
    __tablename__ = 'procuradores'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)

# ------------------------
# MODELO: Asistente
# ------------------------
class Asistente(Usuario):
    __tablename__ = 'asistentes'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
