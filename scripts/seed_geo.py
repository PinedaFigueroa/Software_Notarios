# scripts/seed_geo.py
# --- add project root to sys.path ---
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ------------------------------------

from app import create_app, db
from app.models.geo import Country, Admin1Division, Admin2Division, NationalIDRule
import csv, re

# --------- helpers de upsert ----------
def upsert_country(iso2: str, name: str, iso3: str | None = None):
    c = Country.query.filter_by(iso2=iso2).first()
    if not c:
        c = Country(iso2=iso2, name=name, iso3=iso3)
        db.session.add(c)
    else:
        c.name, c.iso3 = name, iso3
    return c

def upsert_admin1(country: Country, code: str, name: str, type_name: str = "Departamento"):
    code = re.sub(r"\D", "", code or "").zfill(2)
    r = Admin1Division.query.filter_by(country_id=country.id, code=code).first()
    if not r:
        r = Admin1Division(country_id=country.id, code=code, name=name.strip(), type_name=type_name)
        db.session.add(r)
    else:
        r.name, r.type_name = name.strip(), type_name
    return r

def upsert_admin2(country: Country, admin1: Admin1Division, code: str, name: str, type_name: str = "Municipio"):
    code = re.sub(r"\D", "", code or "").zfill(2) if name.strip() else ""
    m = Admin2Division.query.filter_by(country_id=country.id, admin1_id=admin1.id, code=code).first()
    if not m:
        m = Admin2Division(country_id=country.id, admin1_id=admin1.id, code=code, name=name.strip(), type_name=type_name)
        db.session.add(m)
    else:
        m.name, m.type_name = name.strip(), type_name
    return m

def upsert_rule(country: Country, id_type: str, name: str, regex: str,
                dept_from_end: int, dept_len: int, muni_from_end: int, muni_len: int, notes: str = ""):
    r = NationalIDRule.query.filter_by(country_id=country.id, id_type=id_type).first()
    if not r:
        r = NationalIDRule(country_id=country.id, id_type=id_type, name=name)
        db.session.add(r)
    r.regex = regex
    r.dept_from_end, r.dept_len = dept_from_end, dept_len
    r.muni_from_end, r.muni_len = muni_from_end, muni_len
    r.notes = notes
    return r

# --------- importador CSV ----------
def import_csv(path: str):
    """
    CSV con columnas exactas:
      country_iso2,admin1_code,admin1_name,admin1_type,admin2_code,admin2_name,admin2_type
    Soporta UTF-8 / UTF-8-SIG / CP1252 / Latin-1.
    """
    import csv
    encs = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
    last_err = None
    for enc in encs:
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                rdr = csv.DictReader(f)
                rows = list(rdr)
            break
        except UnicodeDecodeError as e:
            last_err = e
    else:
        raise last_err or RuntimeError(f"No pude leer {path}")

    by_country = {}
    for row in rows:
        iso = (row.get("country_iso2") or "").strip().upper() or "GT"
        admin1_code = (row.get("admin1_code") or "").strip()
        admin1_name = (row.get("admin1_name") or "").strip()
        admin1_type = (row.get("admin1_type") or "Departamento").strip() or "Departamento"
        admin2_code = (row.get("admin2_code") or "").strip()
        admin2_name = (row.get("admin2_name") or "").strip()
        admin2_type = (row.get("admin2_type") or "Municipio").strip() or "Municipio"

        if not admin1_name:
            continue

        if iso not in by_country:
            nice = "Guatemala" if iso == "GT" else iso
            by_country[iso] = upsert_country(iso, nice, "GTM" if iso == "GT" else None)

        c = by_country[iso]
        a1 = upsert_admin1(c, admin1_code, admin1_name, admin1_type)
        if admin2_name:
            upsert_admin2(c, a1, admin2_code, admin2_name, admin2_type)


def main():
    app = create_app()
    with app.app_context():
        # País y regla DPI (GT)
        gt = upsert_country("GT", "Guatemala", "GTM")
        upsert_rule(
            gt, "DPI", "DPI Guatemala",
            regex=r"^\d{13}$",
            dept_from_end=4, dept_len=2,
            muni_from_end=2, muni_len=2,
            notes="Últimos 4 dígitos: 2 depto + 2 muni"
        )

        # IMPORTA CSV COMPLETO
        csv_path = os.path.join("app", "data", "gt_municipios.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No existe {csv_path}. Copia el CSV a esa ruta.")
        import_csv(csv_path)

        db.session.commit()

        # Resumen
        a1_count = Admin1Division.query.filter_by(country_id=gt.id).count()
        a2_count = Admin2Division.query.filter_by(country_id=gt.id).count()
        print(f"Seed OK. Admin1={a1_count}, Admin2={a2_count}")

if __name__ == "__main__":
    main()
