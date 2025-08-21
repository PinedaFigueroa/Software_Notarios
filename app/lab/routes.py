# app/lab/routes.py
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError
from . import lab_bp
from .forms import NitDpiForm
from app import db
from app.models.geo import Country, Admin1Division, Admin2Division, NationalIDRule
from app.models.testpersona import TestPersona
import re

# -------------------------------
# Helpers comunes (NIT / DPI)
# -------------------------------
def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def _normalize_dpi(s: str) -> str:
    """13 dígitos sin separadores."""
    return _digits(s)

def _normalize_nit_display(raw: str) -> str:
    """
    Display de NIT:
      - CF / C/F -> 'CF'
      - solo dígitos -> cuerpo-dv (xxxxxxx-x) si hay 2+ dígitos
    """
    s = (raw or "").strip().upper()
    if s in ("CF", "C/F"):
        return "CF"
    d = _digits(s)
    if len(d) >= 2:
        return f"{d[:-1]}-{d[-1]}"
    return d or s

def _nit_uq_value(raw: str):
    """
    Canon para unicidad de NIT:
      - CF/C-F -> None (permite repetidos)
      - resto  -> solo dígitos (mismo NIT sin guiones = duplicado)
    """
    s = (raw or "").strip().upper()
    if s in ("CF", "C/F"):
        return None
    return _digits(s)

# -------------------------------
# DPI → Depto/Muni vía reglas geo
# -------------------------------
def _dpi_extract_with_rule(country_iso2: str, id_type: str, id_value: str):
    """
    Usa NationalIDRule para extraer códigos admin1/admin2 de un ID normalizado.
    Retorna (dept_code, muni_code, dept_name, muni_name) o (None, None, None, None).
    """
    digits = _digits(id_value)
    country = Country.query.filter_by(iso2=country_iso2).first()
    rule = NationalIDRule.query.filter_by(country_id=country.id, id_type=id_type).first() if country else None
    if not (country and rule and rule.dept_from_end and rule.dept_len and
            rule.muni_from_end and rule.muni_len and len(digits) >= max(rule.dept_from_end, rule.muni_from_end)):
        return None, None, None, None

    d_start = len(digits) - rule.dept_from_end
    m_start = len(digits) - rule.muni_from_end
    
# Asegura padding exacto (2 dígitos para GT)
    dept_code = digits[d_start:d_start + rule.dept_len].zfill(rule.dept_len)
    muni_code = digits[m_start:m_start + rule.muni_len].zfill(rule.muni_len)

    a1 = Admin1Division.query.filter_by(country_id=country.id, code=dept_code).first()
    a2 = Admin2Division.query.filter_by(country_id=country.id, admin1_id=a1.id if a1 else None, code=muni_code).first()
    
    return dept_code, muni_code, (a1.name if a1 else None), (a2.name if a2 else None)

# -------------------------------
# Rutas de laboratorio
# -------------------------------
@lab_bp.route("/lab/ping")
def ping():
    return "lab OK", 200

@lab_bp.route("/lab/nit-dpi", methods=["GET", "POST"])
def lab_nit_dpi():
    form = NitDpiForm()
    found = {"dept_code": None, "muni_code": None, "dept_name": None, "muni_name": None}

    # Resolver Depto/Muni si hay un DPI presente (GET con valor o POST inválido)
    raw_dpi = getattr(form.dpi, "data", None)
    if raw_dpi:
        dc, mc, dn, mn = _dpi_extract_with_rule("GT", "DPI", raw_dpi)
        found.update({"dept_code": dc, "muni_code": mc, "dept_name": dn, "muni_name": mn})

    if form.validate_on_submit():
        name = (form.name.data or "").strip()
        nit_display = _normalize_nit_display(form.nit.data)
        nit_uq = _nit_uq_value(form.nit.data)
        dpi = _normalize_dpi(form.dpi.data)

        rec = TestPersona(name=name, nit=nit_display, nit_uq=nit_uq, dpi=dpi)
        db.session.add(rec)
        try:
            db.session.commit()
            flash(f"Guardado OK: {rec}", "success")
            return redirect(url_for("lab.lab_nit_dpi"))
        except IntegrityError:
            db.session.rollback()
            flash("NIT (real) o DPI ya existe.", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {e}", "danger")

    last = TestPersona.query.order_by(TestPersona.id.desc()).limit(10).all()
    return render_template("lab/nit_dpi_form.html", form=form, last=last, found=found)

from flask import request

@lab_bp.route("/lab/test-personas")
def lab_test_personas():
    # límite rápido por defecto; usa ?all=1 para traer todo
    q = TestPersona.query.order_by(TestPersona.id.desc())
    if request.args.get("all"):
        rows = q.all()
        showing = len(rows)
    else:
        limit = request.args.get("limit", "200")
        try:
            n = max(1, min(2000, int(limit)))
        except Exception:
            n = 200
        rows = q.limit(n).all()
        showing = len(rows)

    items = []
    for r in rows:
        dc, mc, dn, mn = _dpi_extract_with_rule("GT", "DPI", r.dpi)
        items.append({
            "id": r.id,
            "name": r.name,
            "nit": r.nit,
            "dpi": r.dpi,
            "dept_code": dc, "dept_name": dn,
            "muni_code": mc, "muni_name": mn,
            "created_at": r.created_at,
        })

    total = q.count()
    return render_template("lab/test_personas_list.html", items=items, total=total, showing=showing)
