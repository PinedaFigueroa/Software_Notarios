# archivo: app/__init__.py
# fecha de creación: 26 / 07 / 25
# cantidad de líneas originales: 40 aprox.
# última actualización: 03 / 08 / 25 hora 22:20
# motivo de la actualización: corregir indentación de return y registrar user_loader
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, login_manager

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor inicia sesión para continuar."

    # Registrar blueprints
    from app.dashboard import dashboard_bp
    from app.auth import auth_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)

    # Registrar comandos personalizados
    from app.cli import cli
    app.cli.add_command(cli)

    # Devolver la app correctamente
    return app


# === User Loader para Flask-Login ===
from app.models.usuarios import Usuario  # Importa al final para evitar circular import

@login_manager.user_loader
def load_user(user_id):
    """Cargar un usuario por ID para Flask-Login."""
    return Usuario.query.get(int(user_id))
