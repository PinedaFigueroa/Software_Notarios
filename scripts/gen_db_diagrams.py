"""
# archivo: scripts/gen_db_diagrams.py
# fecha de creación: 05 / 08 / 25
# cantidad de líneas originales: 60
# última actualización: 05 / 08 / 25 hora 18:25
# motivo de la actualización: Generar diagramas ER en PNG y PDF con ERAlchemy
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-
"""
import os
import subprocess
from datetime import datetime

# --- Configuración de la base de datos ---
DB_URI = "postgresql+psycopg2://default:12345678@localhost:5432/software_notarios"

# --- Directorio de salida ---
output_dir = "db_docs/Diagramas"
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
png_file = os.path.join(output_dir, f"ERD_{timestamp}.png")
pdf_file = os.path.join(output_dir, f"ERD_{timestamp}.pdf")

print("=== Generando diagramas ER ===")

try:
    # PNG
    print("Generando diagrama ER en PNG...")
    subprocess.run(["eralchemy", "-i", DB_URI, "-o", png_file], check=True)

    # PDF
    print("Generando diagrama ER en PDF...")
    subprocess.run(["eralchemy", "-i", DB_URI, "-o", pdf_file], check=True)

    print("Diagramas ER generados en:", output_dir)
except Exception as e:
    print("❌ Error generando diagramas ER:", e)
