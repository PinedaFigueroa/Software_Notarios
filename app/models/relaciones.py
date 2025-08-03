# archivo: app/models/relaciones.py
# fecha de creación: 15 / 07 / 25 hora 09:45
# cantidad de lineas originales: ~10
# ultima actualización:
# motivo de la actualización: relación notario-procurador
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Tabla de relación entre notarios, procuradores y asistentes
"""

from app.extensions import db

class NotarioProcurador(db.Model):
    __tablename__ = 'notario_procurador'
    id = db.Column(db.Integer, primary_key=True)
    notario_id = db.Column(db.Integer, db.ForeignKey('notarios.id'))
    procurador_id = db.Column(db.Integer, db.ForeignKey('procuradores.id'))

class NotarioAsistente(db.Model):
    __tablename__ = 'notario_asistente'
    id = db.Column(db.Integer, primary_key=True)
    notario_id = db.Column(db.Integer, db.ForeignKey('notarios.id'))
    asistente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))