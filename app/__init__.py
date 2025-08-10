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

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message_category = 'warning'

    # Cargar modelo Usuario para el user_loader
    from app.models.usuarios import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Usuario.query.get(int(user_id))
        except Exception:
            return None

    # Blueprints
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.superadmin import superadmin_bp
    app.register_blueprint(superadmin_bp)

    return app
