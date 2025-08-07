"""
# archivo: scripts/gen_diagrama_multipage_color.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 90 aprox.
# última actualización: 05 / 08 / 25 hora 17:45
# motivo de la actualización: Multipágina 4x4 en color con selección automática del PNG más reciente
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-
"""
import os
import glob
import math
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# === Configuración ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAM_DIR = os.path.join(BASE_DIR, "db_docs", "Diagramas")
GRID_ROWS = 4
GRID_COLS = 4
MARGIN = 2.5 * cm
PAGE_WIDTH, PAGE_HEIGHT = letter

# Buscar automáticamente el PNG de diagrama a color más reciente
pattern = os.path.join(DIAGRAM_DIR, "ERD_COLORES_*.png")
png_files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

if not png_files:
    print("❌ ERROR: No se encontró ningún archivo ERD_COLOR_*.png en db_docs/Diagramas/")
    exit(1)

IMG_FILE = png_files[0]
print(f"🎨 Usando imagen más reciente: {IMG_FILE}")

# Crear nombre de salida
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
OUTPUT_FILE = os.path.join(DIAGRAM_DIR, f"ERD_MULTIPAGE_COLOR_{timestamp}_4x4.pdf")

# === Abrir imagen base ===
img = Image.open(IMG_FILE).convert("RGB")
img_width, img_height = img.size

# === Calcular tamaño por página ===
usable_width = PAGE_WIDTH - 2*MARGIN
usable_height = PAGE_HEIGHT - 2*MARGIN
tile_width = usable_width
tile_height = usable_height

# Calcular tamaño de cada recorte
tile_px_width = img_width / GRID_COLS
tile_px_height = img_height / GRID_ROWS

# === Crear PDF multipágina ===
c = canvas.Canvas(OUTPUT_FILE, pagesize=letter)

total_pages = GRID_ROWS * GRID_COLS
page_count = 0

for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        x0 = col * tile_px_width
        y0 = row * tile_px_height
        x1 = x0 + tile_px_width
        y1 = y0 + tile_px_height

        # Crop
        tile = img.crop((x0, y0, x1, y1))

        # Guardar tile temporal
        temp_tile = os.path.join(DIAGRAM_DIR, f"_tile_color_{row}_{col}.png")
        tile.save(temp_tile)

        # Nueva página
        page_count += 1
        c.drawImage(temp_tile, MARGIN, MARGIN, width=usable_width, height=usable_height)

        # Encabezado y pie de página
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT-1*cm, "Base de Datos Software Notarios")
        c.setFont("Helvetica", 8)
        c.drawCentredString(PAGE_WIDTH/2, 1*cm, f"Página {page_count} de {total_pages} - Generado {timestamp}")

        c.showPage()

c.save()

print(f"✅ PDF multipágina en color generado: {OUTPUT_FILE}")
