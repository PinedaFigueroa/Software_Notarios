# archivo: scripts/gen_diagrama_simple.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 25
# última actualización: 05 / 08 / 25 hora 21:41
# motivo de la creación: Generar un solo diagrama ER funcional, sin pasos extra
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import subprocess

# Conexión a PostgreSQL
DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"

# Carpeta de salida
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
os.makedirs("db_docs/Diagramas", exist_ok=True)
OUTPUT_PNG = f"db_docs/Diagramas/ERD_SIMPLE_{timestamp}.png"

# Comando simple con ERAlchemy
print("Generando diagrama ER con ERAlchemy...")
try:
    subprocess.run(["eralchemy", "-i", DB_URI, "-o", OUTPUT_PNG], check=True)
    print("Diagrama generado correctamente en:", OUTPUT_PNG)
except Exception as e:
    print("Error al generar el diagrama:", e)
