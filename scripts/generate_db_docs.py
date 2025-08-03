# archivo: scripts/generate_db_docs.py
# fecha de creación: 03 / 08 / 25
# cantidad de líneas originales: 80 aprox.
# última actualización: 03 / 08 / 25 hora 22:30
# motivo de la actualización: corregir uso de create_schema_graph con engine y metadata
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pandas as pd
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy_schemadisplay import create_schema_graph
from app import create_app
from app.extensions import db

def generate_db_docs(output_dir="db_docs"):
    """Genera documentación visual y tabular de la BDD."""
    app = create_app()
    with app.app_context():
        # Crear carpeta de salida
        os.makedirs(output_dir, exist_ok=True)

        # Obtener metadata y engine
        engine = db.engine
        metadata = db.metadata
        metadata.reflect(bind=engine)

        # 1️⃣ Generar esquema gráfico grande
        graph = create_schema_graph(
            engine=engine,
            metadata=metadata,
            show_datatypes=True,
            show_indexes=True,
            rankdir='LR',        # horizontal para esquemas grandes
            concentrate=False
        )
        graph_file = os.path.join(output_dir, "db_schema_full.png")
        graph.write_png(graph_file)
        print(f"✅ Esquema gráfico generado en {graph_file}")

        # 2️⃣ Generar listado completo de tablas y columnas
        inspector = inspect(engine)
        tables_data = []
        for table_name in inspector.get_table_names():
            for column in inspector.get_columns(table_name):
                tables_data.append({
                    "Tabla": table_name,
                    "Columna": column["name"],
                    "Tipo": str(column["type"]),
                    "Nullable": column["nullable"],
                    "Default": column["default"]
                })

        df = pd.DataFrame(tables_data)
        csv_file = os.path.join(output_dir, "db_tables_list.csv")
        xlsx_file = os.path.join(output_dir, "db_tables_list.xlsx")

        df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        df.to_excel(xlsx_file, index=False)
        print(f"✅ Listado de tablas exportado a {csv_file} y {xlsx_file}")


if __name__ == "__main__":
    generate_db_docs()
