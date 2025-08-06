# archivo: scripts/gen_diagrama_colores_advanced.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 70 aprox.
# última actualización: 05 / 08 / 25 hora 17:05
# motivo de la actualización: Generación de diagrama ER en colores usando Graphviz
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from graphviz import Digraph

# --- Configuración ---
DB_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/software_notarios"
OUTPUT_DIR = "db_docs/Diagramas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
PNG_FILE = os.path.join(OUTPUT_DIR, f"ERD_COLORES_{timestamp}.png")
PDF_FILE = os.path.join(OUTPUT_DIR, f"ERD_COLORES_{timestamp}.pdf")

print("🎨 Generando diagrama ER a color con Graphviz...")

# --- Conectar a la BDD y obtener metadatos ---
engine = create_engine(DB_URI)
metadata = MetaData()
metadata.reflect(bind=engine)

# --- Configuración de colores por categoría ---
color_map = {
    "usuarios": "#8FBC8F",    # Verde suave
    "documentos": "#87CEEB",  # Azul claro
    "pagos": "#FFD700",       # Dorado
    "default": "#D3D3D3"      # Gris claro
}

def get_color_for_table(table_name):
    t = table_name.lower()
    if "usuario" in t or "notario" in t or "procurador" in t:
        return color_map["usuarios"]
    elif "doc" in t or "acta" in t or "clausula" in t:
        return color_map["documentos"]
    elif "pago" in t or "plan" in t or "factura" in t:
        return color_map["pagos"]
    else:
        return color_map["default"]

# --- Crear diagrama ---
dot = Digraph("ERD_Colores", format="png")
dot.attr(rankdir="LR", splines="ortho", nodesep="0.8", ranksep="1.0")

# Agregar nodos (tablas)
for table_name, table in metadata.tables.items():
    color = get_color_for_table(table_name)
    label = f"<<B>{table_name}</B><BR/>" + "<BR/>".join([c.name for c in table.columns]) + ">"
    dot.node(table_name, label=label, shape="box", style="filled,rounded", fillcolor=color, fontname="Helvetica")

# Agregar relaciones
for table_name, table in metadata.tables.items():
    for fk in table.foreign_keys:
        dot.edge(table_name, fk.column.table.name, color="#555555")

# --- Guardar archivos ---
dot.render(PNG_FILE.replace(".png", ""), cleanup=True)
dot.format = "pdf"
dot.render(PDF_FILE.replace(".pdf", ""), cleanup=True)

print(f"✅ Diagramas en colores generados:")
print(f" {PNG_FILE}")
print(f" {PDF_FILE}")
