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
# import datetime  # se probará importar todo de core, si funciona quitar estas lineas
# from app import db
# from sqlalchemy.orm import relationship
# from sqlalchemy import Enum, Boolean, ForeignKey, DateTime

from app.models.core import * 
#------------------------
# MODELO: BufeteJuridico
# ------------------------
class BufeteJuridico(db.Model):
    __tablename__ = 'bufetes_juridicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_bufete = db.Column(db.String(255), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    nit = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)

    # Personalización de marca y aplicación SI EN EL FUTURO SE CONCESIONA
    # app_copyright = db.Column(db.String(255), nullable=True)
    # nombre_aplicacion = db.Column(db.String(255), nullable=True)

    # Configuración y permisos para lo que ha elegido
    # feature flags, 
    maneja_inventario_timbres_papel = db.Column(Boolean, default=True, nullable=False)
    incluye_libreria_plantillas_inicial = db.Column(Boolean, default=True, nullable=False)
    habilita_auditoria_borrado_logico = db.Column(Boolean, default=True, nullable=False)
    habilita_dashboard_avanzado = db.Column(Boolean, default=True, nullable=False)
    # esta ayuda deben tenerla todos, se puso acá pero es parte de lo necesario
    habilita_ayuda_contextual = db.Column(Boolean, default=True, nullable=False)
    # esto digital servirá cuando se exporte el sw o cambie la ley en Guatemala
    habilita_papeleria_digital = db.Column(Boolean, default=True, nullable=False)
    
    # este campo hizo falta en determinado momento, como contactar al bufete
    forma_contacto = db.Column(db.String(255), nullable=True)

    # Facturación por uso de la apliación
    facturacion_nombre = db.Column(db.String(255), nullable=True)
    facturacion_nit = db.Column(db.String(50), nullable=True)
    facturacion_direccion = db.Column(db.String(255), nullable=True)

    # Métodos de pago del bufete
    formas_pago = db.Column(db.String(150), nullable=True)  # ejemplo: "efectivo,tarjeta,transferencia"
    metodo_pago_preferido = db.Column(db.String(50), nullable=True)

    # Control si no ha pagado, si se borra lógicamente
    activo = db.Column(Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
    plan = relationship('Plan', back_populates='bufetes')

    usuarios = relationship('Usuario', back_populates='bufete', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Bufete %s>" % self.nombre_bufete_o_razon_social
