from datetime import datetime

# archivo: app/models/libreria.py
# última actualización: 26 / 07 / 25 hora 17:00
# motivo de la actualización: limpieza de uso redundante de datetime.datetime.utcnow
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

fecha_creacion = Column(DateTime, default=datetime.utcnow)
