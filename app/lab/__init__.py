
from flask import Blueprint

# Nombre del blueprint = 'lab'  → endpoints 'lab.*'
lab_bp = Blueprint("lab", __name__, template_folder="templates")

# 🚨 IMPORTANTE: importa las rutas para que se registren en este blueprint
from . import routes  # noqa: F401
