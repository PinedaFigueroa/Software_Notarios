# archivo: app/__init__.py
# fecha de creación: 26 / 07 / 25
# cantidad de líneas originales: 48
# última actualización: 07 / 08 / 25 hora 19:00
# motivo de la actualización: Uso de core_ext para evitar ciclos y limpiar imports
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Inicializa la aplicación Flask, configuraciones, extensiones y blueprints.
"""

from flask import Flask
from flask_login import LoginManager
from app.core_ext import db, migrate
from app.models.usuarios import Usuario

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.login_message = 'Debes iniciar sesión para continuar.'
login_manager.login_message_category = 'warning'

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.superadmin import superadmin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(superadmin_bp)

    # CLI personalizada
    from app.cli import cli
    app.cli.add_command(cli)

    return app
