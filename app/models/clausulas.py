from datetime import datetime

# archivo: app/models/clausulas.py
# última actualización: 26 / 07 / 25 hora 17:00
# motivo de la actualización: limpieza de uso redundante de datetime.datetime.utcnow
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

# Ejemplo de uso corregido
fecha_creacion = Column(DateTime, default=datetime.utcnow)
fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
