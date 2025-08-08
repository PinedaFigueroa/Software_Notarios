# archivo: app/core_ext.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 8
# última actualización: 07 / 08 / 25 hora 19:00
# motivo de la creación: Declaración única de extensiones db y migrate
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
