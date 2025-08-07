# archivo: scripts/gen_db_docs.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 60 aprox.
# última actualización: 05 / 08 / 25 hora 17:15
# motivo de la actualización: Generar Excel de tablas y columnas con PostgreSQL
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import pandas as pd
from sqlalchemy import create_engine, inspect

DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"
OUTPUT_DIR = os.path.join("db_docs", "Listados")
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = create_engine(DB_URI)
insp = inspect(engine)

tables_data = []
for table_name in insp.get_table_names():
    columns = insp.get_columns(table_name)
    for col in columns:
        tables_data.append({
            "Tabla": table_name,
            "Columna": col['name'],
            "Tipo": str(col['type']),
            "PK": col.get('primary_key', False),
            "Nullable": col.get('nullable', True)
        })

if tables_data:
    import datetime
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_path = os.path.join(OUTPUT_DIR, f"listado_tablas_{ts}.xlsx")
    df = pd.DataFrame(tables_data)
    df.to_excel(file_path, index=False)
    print(f"✅ Listado generado en {file_path}")
else:
    print("⚠ No se encontraron tablas en la base de datos.")
