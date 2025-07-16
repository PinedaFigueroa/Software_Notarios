# archivo: app/__init__.py
# fecha de creación: 14 / 07 / 25
# cantidad de lineas originales: ____
# última actualización: 15 / 07 / 25 hora 08:20
# motivo de la actualización: evitar circular import con cli.py
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config.from_object('app.config.Config')

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa y registra blueprints aquí si tienes

    # Importa y registra comandos CLI al final para evitar circular import
    from app.cli import cli
    app.cli.add_command(cli)

    return app
