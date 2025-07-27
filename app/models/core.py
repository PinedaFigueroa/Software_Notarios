from datetime import datetime

# archivo: app/models/core.py
# última actualización: 26 / 07 / 25 hora 17:00
# motivo de la actualización: limpieza de uso redundante de datetime.datetime.utcnow
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

# Simulación de modelos
fecha_creacion = Column(DateTime, default=datetime.utcnow)
