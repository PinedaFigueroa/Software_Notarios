# app/models/geo.py
# creado 18 - 08 -25
# objetivo tener control por pais de los diferentes DPIs
# última actualización: 18 - 08 - 25
from app import db

class Country(db.Model):
    __tablename__ = "geo_countries"
    id    = db.Column(db.Integer, primary_key=True)
    iso2  = db.Column(db.String(2),  unique=True, nullable=False, index=True)  # GT, MX, BR, AR, CO...
    iso3  = db.Column(db.String(3),  unique=True, nullable=True)
    name  = db.Column(db.String(120), nullable=False)

class Admin1Division(db.Model):
    __tablename__ = "geo_admin1"
    id         = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("geo_countries.id", ondelete="CASCADE"), nullable=False)
    code       = db.Column(db.String(10), nullable=False)   # "01" .. "22" (GT) / "JAL" (MX) / etc.
    name       = db.Column(db.String(120), nullable=False)  # Departamento / Estado / Provincia nombre
    type_name  = db.Column(db.String(40), nullable=True)    # "Departamento", "Estado", "Provincia"...
    __table_args__ = (db.UniqueConstraint("country_id", "code", name="uq_admin1_country_code"),)
    country = db.relationship("Country", backref=db.backref("admin1s", lazy="dynamic", cascade="all, delete"))

class Admin2Division(db.Model):
    __tablename__ = "geo_admin2"
    id         = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("geo_countries.id", ondelete="CASCADE"), nullable=False)
    admin1_id  = db.Column(db.Integer, db.ForeignKey("geo_admin1.id", ondelete="CASCADE"), nullable=False)
    code       = db.Column(db.String(10), nullable=False)   # "01".."xx" por cada admin1
    name       = db.Column(db.String(120), nullable=False)  # Municipio / Condado / Partido...
    type_name  = db.Column(db.String(40), nullable=True)
    __table_args__ = (db.UniqueConstraint("country_id", "admin1_id", "code", name="uq_admin2_country_admin1_code"),)
    country = db.relationship("Country")
    admin1  = db.relationship("Admin1Division", backref=db.backref("admin2s", lazy="dynamic", cascade="all, delete"))

class NationalIDRule(db.Model):
    """
    Reglas para parsear y validar IDs nacionales por país.
    Ej. GT-DPI: últimos 4 dígitos = 2 depto + 2 muni.
    """
    __tablename__ = "national_id_rules"
    id         = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("geo_countries.id", ondelete="CASCADE"), nullable=False)
    id_type    = db.Column(db.String(20), nullable=False)  # 'DPI', 'CURP', 'DNI', etc.
    name       = db.Column(db.String(80), nullable=False)  # etiqueta humana
    regex      = db.Column(db.String(200), nullable=True)  # patrón base (solo dígitos, longitud, etc.)

    # offsets desde el final de la cadena normalizada (solo dígitos):
    dept_from_end = db.Column(db.Integer, nullable=True)  # p.ej. 4 (empieza a 4 del final)
    dept_len      = db.Column(db.Integer, nullable=True)  # p.ej. 2
    muni_from_end = db.Column(db.Integer, nullable=True)  # p.ej. 2
    muni_len      = db.Column(db.Integer, nullable=True)  # p.ej. 2

    notes = db.Column(db.Text)
    country = db.relationship("Country")
    __table_args__ = (db.UniqueConstraint("country_id", "id_type", name="uq_country_idtype"),)
