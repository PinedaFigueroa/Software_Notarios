# scripts/clear_lab.py
# limpia las tablas para pruebas
# creado 18 - 08 - 25
# última modificación: 18 - 08 - 25
# --- add project root to sys.path ---
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------

from app import create_app, db
from sqlalchemy import delete
from app.models.testpersona import TestPersona

def main():
    app = create_app()
    with app.app_context():
        db.session.execute(delete(TestPersona))
        db.session.commit()
        print("Limpiado: test_personas")

if __name__ == "__main__":
    main()
