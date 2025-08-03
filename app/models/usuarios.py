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
- BufeteJuridico: Datos del bufete, plan, formas de pago, feature flags.
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

from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, Boolean, DateTime, ForeignKey
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum
from flask_login import UserMixin
import datetime

# ------------------------
# MODELO: BufeteJuridico
# ------------------------
class BufeteJuridico(db.Model):
    __tablename__ = 'bufetes_juridicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_bufete_o_razon_social = db.Column(db.String(255), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    nit = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)

    # Personalización de marca y aplicación
    app_copyright = db.Column(db.String(255), nullable=True)
    nombre_aplicacion = db.Column(db.String(255), nullable=True)

    # Configuración y permisos
    maneja_inventario_timbres_papel = db.Column(Boolean, default=True, nullable=False)
    incluye_libreria_plantillas_inicial = db.Column(Boolean, default=True, nullable=False)
    habilita_auditoria_borrado_logico = db.Column(Boolean, default=True, nullable=False)
    habilita_dashboard_avanzado = db.Column(Boolean, default=True, nullable=False)
    habilita_ayuda_contextual = db.Column(Boolean, default=True, nullable=False)

    # Facturación
    facturacion_nombre = db.Column(db.String(255), nullable=True)
    facturacion_nit = db.Column(db.String(50), nullable=True)
    facturacion_direccion = db.Column(db.String(255), nullable=True)

    # Métodos de pago del bufete
    formas_pago = db.Column(db.String(150), nullable=True)  # ejemplo: "efectivo,tarjeta,transferencia"
    metodo_pago_preferido = db.Column(db.String(50), nullable=True)

    # Control
    activo = db.Column(Boolean, default=True)
    fecha_creacion = db.Column(DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
    plan = relationship('Plan', back_populates='bufetes')

    usuarios = relationship('Usuario', back_populates='bufete', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Bufete %s>" % self.nombre_bufete_o_razon_social

# ------------------------
# MODELO: Usuario base
# ------------------------
class Usuario(db.Model):
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
