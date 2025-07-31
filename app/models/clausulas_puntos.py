# archivo: app/models/clausulas_puntos.py
# fecha de creación: 29 / 07 / 25
# cantidad de líneas originales: ~40
# última actualización: 29 / 07 / 25 hora 12:40
# motivo de la creación: modelo unificado para cláusulas y puntos de acta
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from datetime import datetime
from app.models.enums import TipoClausulaEnum, TipoAplicacionClausulaEnum

class ClausulasPuntos(db.Model):
    """
    Modelo unificado para Cláusulas (escrituras) y Puntos de Acta.
    Permite registrar contenido legal reutilizable en documentos y actas.
    
    - nombre: nombre de la cláusula/punto (ej. 'PRIMERO: REQUERIMIENTO')
    - contenido: texto completo
    - fundamento_legal / fundamento_doctrinario: soporte jurídico
    - instrumentos_permitidos: opcional, en qué instrumentos se sugiere
    - tipo: tipo de cláusula (general, obligatoria, sugerida, personalizada)
    - aplicacion: si aplica a documentos, actas o ambos
    - activo: para permitir baja lógica sin borrar el registro
    - fecha_creacion: auditoría básica
    """

    __tablename__ = 'clausulas_puntos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fundamento_legal = Column(Text, nullable=True)
    fundamento_doctrinario = Column(Text, nullable=True)
    instrumentos_permitidos = Column(String(255), nullable=True)

    tipo = Column(Enum(TipoClausulaEnum), nullable=False)
    aplicacion = Column(Enum(TipoAplicacionClausulaEnum), nullable=False, default=TipoAplicacionClausulaEnum.AMBOS)

    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ClausulasPuntos {self.nombre} ({self.tipo.value})>"
