# archivo: app/__init__.py
# fecha de creación: 26 / 07 / 25
# cantidad de líneas originales: 40 aprox.
# última actualización: 27 / 07 / 25 hora 21:40
# motivo de la actualización: registrar correctamente blueprint del dashboard
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Registrar blueprints
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar comandos personalizados
    from app.cli import cli
    app.cli.add_command(cli)

    return app
