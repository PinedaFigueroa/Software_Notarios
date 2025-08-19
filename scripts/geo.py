# scripts/seed_geo.py
# objetivo:  alimentar las tablas geo_country geo_admin
# creado: 18 - 08 - 25 
# actualizado: 18 - 08 - 25

from app import create_app, db
from app.models.geo import Country, Admin1Division, Admin2Division, NationalIDRule
import csv, os, re

def upsert_country(iso2, name, iso3=None):
    c = Country.query.filter_by(iso2=iso2).first()
    if not c:
        c = Country(iso2=iso2, name=name, iso3=iso3)
        db.session.add(c)
    else:
        c.name, c.iso3 = name, iso3
    return c

def upsert_admin1(country, code, name, type_name="Departamento"):
    r = Admin1Division.query.filter_by(country_id=country.id, code=code).first()
    if not r:
        r = Admin1Division(country_id=country.id, code=code, name=name, type_name=type_name)
        db.session.add(r)
    else:
        r.name, r.type_name = name, type_name
    return r

def upsert_admin2(country, admin1, code, name, type_name="Municipio"):
    m = Admin2Division.query.filter_by(country_id=country.id, admin1_id=admin1.id, code=code).first()
    if not m:
        m = Admin2Division(country_id=country.id, admin1_id=admin1.id, code=code, name=name, type_name=type_name)
        db.session.add(m)
    else:
        m.name, m.type_name = name, type_name
    return m

def upsert_rule(country, id_type, name, regex, dept_from_end, dept_len, muni_from_end, muni_len, notes=""):
    r = NationalIDRule.query.filter_by(country_id=country.id, id_type=id_type).first()
    if not r:
        r = NationalIDRule(country_id=country.id, id_type=id_type, name=name)
        db.session.add(r)
    r.regex = regex
    r.dept_from_end, r.dept_len = dept_from_end, dept_len
    r.muni_from_end, r.muni_len = muni_from_end, muni_len
    r.notes = notes
    return r

def seed_gt_minimal():
    gt = upsert_country("GT", "Guatemala", "GTM")
    # Regla DPI GT: últimos 4 dígitos → 2 dept + 2 muni
    upsert_rule(
        gt, "DPI", "DPI Guatemala",
        regex=r"^\d{13}$",
        dept_from_end=4, dept_len=2,
        muni_from_end=2, muni_len=2,
        notes="Últimos 4 dígitos: 2 depto + 2 muni"
    )

    # Mínimo de prueba (rellena luego con CSV completo)
    gua = upsert_admin1(gt, "01", "Guatemala", "Departamento")
    upsert_admin2(gt, gua, "01", "Guatemala", "Municipio")
    upsert_admin2(gt, gua, "02", "Mixco", "Municipio")
    sac = upsert_admin1(gt, "03", "Sacatepéquez", "Departamento")
    upsert_admin2(gt, sac, "01", "Antigua Guatemala", "Municipio")

def import_csv(path):
    """
    CSV esperado con columnas:
    country_iso2,admin1_code,admin1_name,admin1_type,admin2_code,admin2_name,admin2_type
    """
    with open(path, "r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
    by_country = {}
    for row in rows:
        iso = row["country_iso2"].strip().upper()
        if iso not in by_country:
            by_country[iso] = upsert_country(iso, iso)  # name temporal; luego lo actualizas
        c = by_country[iso]
        a1 = upsert_admin1(c, row["admin1_code"].strip(), row["admin1_name"].strip(), row.get("admin1_type") or None)
        upsert_admin2(c, a1, row["admin2_code"].strip(), row["admin2_name"].strip(), row.get("admin2_type") or None)

def main():
    app = create_app()
    with app.app_context():
        # Seed mínimo GT
        seed_gt_minimal()

        # Si tienes un CSV completo, descomenta y ajusta la ruta:
        # import_csv("app/data/gt_municipios.csv")

        db.session.commit()
        print("Seed OK")

if __name__ == "__main__":
    main()
