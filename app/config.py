
# archivo: app/config.py
# fecha de creación: 15 / 07 / 25 hora 08:30
# cantidad de lineas originales: ~20
# última actualización:
# motivo de la actualización: crear clase Config para la app Flask
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

import os

class Config:
    # Clave secreta (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:12345678@localhost:5432/software_notarios'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Otros flags de la app
    DEBUG = True
