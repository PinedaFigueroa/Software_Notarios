# -*- coding: utf-8 -*-
# archivo: app/models/core.py
# autor: Proyecto Software_Notarios & Tars-90
# última actualización: 25 / 07 / 25
# Descripción: Modelo central que define bufetes y usuarios

from app import db
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.models.enums import EstadoUsuarioEnum, RolUsuarioEnum

class BufeteJuridico(db.Model):
    """
    Representa a cada bufete de notarios que contrata el sistema.
    Incluye datos de contacto, facturación y relación con usuarios.
    """
    __tablename__ = 'bufetes_juridicos'

    id = Column(Integer, primary_key=True)

    # Datos obligatorios
    nombre_bufete_o_razon_social = Column(String(255), unique=True, nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=False)

    # Opcionales
    nit = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    forma_contacto_preferida = Column(String(100), nullable=True)

    # Personalización
    app_copyright = Column(String(255), nullable=True)  # Solo para bufete principal
    nombre_aplicacion = Column(String(255), nullable=True)

    # Facturación (solo editable por superadmin)
    facturacion_nombre = Column(String(255), nullable=True)
    facturacion_nit = Column(String(50), nullable=True)
    facturacion_direccion = Column(String(255), nullable=True)
    facturacion_razon = Column(String(255), nullable=True)

    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    plan_id = Column(Integer, ForeignKey('planes.id'))
    plan = relationship('Plan', back_populates='bufetes')

    notarios = relationship('Notario', back_populates='bufete')
    procuradores = relationship('Procurador', back_populates='bufete')
    asistentes = relationship('Asistente', back_populates='bufete')  

    # Feature flags
    habilita_inventario = Column(Boolean, default=False)
    habilita_auditoria = Column(Boolean, default=False)
    habilita_trazabilidad = Column(Boolean, default=False)
    # Agrega otros que quieras controlar

    def __repr__(self):
        return f"<BufeteJuridico(id={self.id}, nombre='{self.nombre_bufete_o_razon_social}')>"


class UsuarioSistema(db.Model):
    """
    Usuarios que acceden al sistema: superadmin, admin interno del bufete, notarios, etc.
    """
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
    """
    Notarios del bufete.
    """
    __tablename__ = 'notarios'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    colegiado = Column(String(50), unique=True, nullable=False)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    bufete = relationship('BufeteJuridico', back_populates='notarios')


class Procurador(db.Model):
    """
    Procuradores del bufete.
    """
    __tablename__ = 'procuradores'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    dpi = Column(String(13), unique=True, nullable=False)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    bufete = relationship('BufeteJuridico', back_populates='procuradores')

class Asistente(db.Model):
    """
    Asistentes que colaboran en el bufete (ejemplo: digitadores, paralegales).
    Pueden tener permisos limitados según el plan y feature flags.
    """
    __tablename__ = 'asistentes'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(150), nullable=True)
    telefono = Column(String(20), nullable=True)

    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    bufete = relationship('BufeteJuridico', back_populates='asistentes')

    def __repr__(self):
        return f"<Asistente(id={self.id}, nombre='{self.nombre_completo}')>"
