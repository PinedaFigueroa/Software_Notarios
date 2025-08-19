# scripts/clear_lab.py

# --- add project root to sys.path ---
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------

from app import create_app, db
from sqlalchemy import delete
from app.models.testpersona import TestPersona
# from app.models.geo import Country, Admin1Division, Admin2Division, NationalIDRule

def main():
    app = create_app()
    with app.app_context():
        db.session.execute(delete(TestPersona))
        # ⚠️ si quieres limpiar geo también:
        # for model in (NationalIDRule, Admin2Division, Admin1Division, Country):
        #     db.session.execute(delete(model))
        db.session.commit()
        print("Limpiado.")
if __name__ == "__main__":
    main()
