# -*- coding: utf-8 -*-
# archivo: app\models\core.py
# fecha de creación: 14 / 07 / 25 hora 23:50
# cantidad de lineas originales: ajusta según tengas
# última actualización: 14 / 07 / 25
# motivo de la actualización: limpieza y coherencia del modelo BufeteJuridico
# líneas actuales: ajusta después de pegar
# autor: Proyecto Software_Notarios & Tars-90

from app import db
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.models.enums import EstadoUsuarioEnum, RolUsuarioEnum

class BufeteJuridico(db.Model):
    __tablename__ = 'bufetes_juridicos'
    id = Column(Integer, primary_key=True)
    
    # Datos básicos del bufete
    nombre_bufete_o_razon_social = Column(String(255), unique=True, nullable=False)  # Ej: "PINEDA VON AHN, FIGUEROA Y ASOCIADOS"
    nit = Column(String(50), nullable=True)  # NIT del bufete (persona jurídica)

    # Contacto
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)

    # Personalización
    app_copyright = Column(String(255), nullable=True)
    nombre_aplicacion = Column(String(255), nullable=True)

    # Control
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    notarios = relationship('Notario', back_populates='bufete')
    procuradores = relationship('Procurador', back_populates='bufete')
    plan_id = Column(Integer, ForeignKey('planes.id'))  # Relación al plan contratado
    plan = relationship('Plan', back_populates='bufetes')


class UsuarioSistema(db.Model):
    __tablename__ = 'usuarios_sistema'
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(150))
    rol = Column(Enum(RolUsuarioEnum), nullable=False)
    estado = Column(Enum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO, nullable=False)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    bufete = relationship('BufeteJuridico')


class Notario(db.Model):
    __tablename__ = 'notarios'
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    colegiado = Column(String(50), unique=True, nullable=False)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)

    bufete = relationship('BufeteJuridico', back_populates='notarios')


class Procurador(db.Model):
    __tablename__ = 'procuradores'
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    dpi = Column(String(13), unique=True, nullable=False)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    bufete = relationship('BufeteJuridico', back_populates='procuradores')
