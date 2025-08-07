# archivo: scripts/gen_db_listings_by_sheet.py
# fecha de creación: 06 / 08 / 25
# motivo: generar Excel con cada tabla en hoja separada
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

import os
import pandas as pd
from sqlalchemy import create_engine, inspect

# --- Configuración de la base de datos ---
DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"

# --- Directorio de salida ---
output_dir = "db_docs/Listados"
os.makedirs(output_dir, exist_ok=True)
OUTPUT_FILE = os.path.join(output_dir, "listado_tablas_por_hoja.xlsx")

print("=== Generando Excel con múltiples hojas por tabla ===")
engine = create_engine(DB_URI)
inspector = inspect(engine)

with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        df = pd.DataFrame([{
            "Columna": col["name"],
            "Tipo": str(col["type"]),
            "Nullable": col["nullable"],
            "Por Defecto": col["default"]
        } for col in columns])
        df.to_excel(writer, sheet_name=table_name[:31], index=False)

print("✅ Archivo Excel generado en:", OUTPUT_FILE)
