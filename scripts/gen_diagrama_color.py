# archivo: scripts/gen_diagrama_color.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 40 aprox.
# última actualización: 05 / 08 / 25 hora 17:15
# motivo de la actualización: Generar diagrama ER en PNG y PDF a color
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import datetime
import subprocess

DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"
OUTPUT_DIR = os.path.join("db_docs", "Diagramas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
png_file = os.path.join(OUTPUT_DIR, f"ERD_COLOR_{timestamp}.png")
pdf_file = os.path.join(OUTPUT_DIR, f"ERD_COLOR_{timestamp}.pdf")

print("🎨 Generando diagrama ER con ERAlchemy...")

try:
    subprocess.run(["eralchemy", "-i", DB_URI, "-o", png_file], check=True)
    subprocess.run(["eralchemy", "-i", DB_URI, "-o", pdf_file], check=True)
    print(f"✅ Diagramas generados:\n {png_file}\n {pdf_file}")
except Exception as e:
    print(f"❌ ERROR generando diagramas: {e}")
