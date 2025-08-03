# archivo: app/__init__.py
# fecha de actualización: 03 / 08 / 25 hora 21:50
# motivo: Integración de Login + Dashboard protegido
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

    # Blueprints
    from app.dashboard import dashboard_bp
    from app.auth import auth_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Redirigir a login si no hay sesión
    login_manager.login_view = 'auth.login'

    # Cargar usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuarios import Usuario
        return Usuario.query.get(int(user_id))

    # CLI
    from app.cli import cli
    app.cli.add_command(cli)

    return app
