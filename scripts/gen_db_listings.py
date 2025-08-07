"""
# archivo: scripts/gen_db_listings.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 40
# última actualización: 05 / 08 / 25 hora 15:20
# motivo de la actualización: Generar Excel con tablas y columnas de la BDD
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*- 
"""
"""
Genera un Excel con todas las tablas y columnas de la base de datos PostgreSQL.
Incluye tipos de datos, si son nulos y valores por defecto.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, inspect

# --- Configuración de la base de datos ---
DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"

# --- Directorio de salida ---
output_dir = "db_docs/Listados"
os.makedirs(output_dir, exist_ok=True)
OUTPUT_FILE = os.path.join(output_dir, "listado_tablas.xlsx")

print("=== Generando listado de tablas y columnas ===")
print("Conectando a la base de datos...")

engine = create_engine(DB_URI)
inspector = inspect(engine)

rows = []
for table_name in inspector.get_table_names():
    for col in inspector.get_columns(table_name):
        rows.append({
            "Tabla": table_name,
            "Columna": col["name"],
            "Tipo": str(col["type"]),
            "Nullable": col["nullable"],
            "Por Defecto": col["default"]
        })

df = pd.DataFrame(rows)
df.to_excel(OUTPUT_FILE, index=False)

print("Archivo Excel generado en:", OUTPUT_FILE)
