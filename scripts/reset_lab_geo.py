# scripts/reset_lab_geo.py
# --- add project root to sys.path ---
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ------------------------------------

from app import create_app, db
from sqlalchemy import delete
from app.models.testpersona import TestPersona
from app.models.geo import Country, Admin1Division, Admin2Division, NationalIDRule
from scripts.seed_geo import main as seed_geo_main  # reutiliza el seed

def reset_all():
    # 1) limpia tablas de prueba (lab)
    db.session.execute(delete(TestPersona))

    # 2) limpia GEO en orden
    db.session.execute(delete(NationalIDRule))
    db.session.execute(delete(Admin2Division))
    db.session.execute(delete(Admin1Division))
    db.session.execute(delete(Country))
    db.session.commit()

    # 3) re-seed GEO desde CSV
    seed_geo_main()

def main():
    app = create_app()
    with app.app_context():
        reset_all()
        print("Reset lab+geo OK.")

if __name__ == "__main__":
    main()
