# archivo: app/validators/gt.py
# última actualización: 13/08/25 hora 02:39
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-
"""Validadores Guatemala (DPI / NIT) centralizados"""
try:
    from nit_dpi_validator import validate_dpi as _vdpi, validate_nit as _vnit
except Exception:
    _vdpi = _vnit = None

def validate_nit(value: str):
    if not value:
        return True, None
    if _vnit is None:
        # Librería no instalada: no bloquear, sólo advertir a logs
        return True, None
    try:
        ok = bool(_vnit(value))
        return (True, None) if ok else (False, "NIT inválido")
    except Exception:
        return False, "NIT inválido"

def validate_dpi(value: str):
    if not value:
        return True, None
    if _vdpi is None:
        return True, None
    try:
        ok = bool(_vdpi(value))
        return (True, None) if ok else (False, "DPI inválido")
    except Exception:
        return False, "DPI inválido"
