from datetime import datetime
from app import db

class TestPersona(db.Model):
    __tablename__ = "test_personas"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)

    # nit YA NO es único
    nit  = db.Column(db.String(32), nullable=False, index=True)

    # nit_uq: ÚNICO solo para NIT reales; será NULL cuando nit sea CF/C-F
    nit_uq = db.Column(db.String(32), unique=True, index=True, nullable=True)

    dpi  = db.Column(db.String(32), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<TestPersona {self.id} {self.name} NIT={self.nit} DPI={self.dpi}>"
