# archivo: scripts/gen_diagrama_multipage.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 60 aprox.
# última actualización: 05 / 08 / 25 hora 17:15
# motivo de la actualización: Generar PDF multipágina 4x4 de diagrama ER
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import math
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import datetime

IMG_FILE = "db_docs/Diagramas/ERD_COLOR_LAST.png"
OUTPUT_FILE = "db_docs/Diagramas/ERD_COLOR_MULTIPAGE.pdf"

# Config multipágina
GRID_ROWS = 4
GRID_COLS = 4
MARGIN = 2.5 * cm
PAGE_WIDTH, PAGE_HEIGHT = letter

# Usar el último PNG generado
diagram_dir = "db_docs/Diagramas"
png_files = [f for f in os.listdir(diagram_dir) if f.endswith(".png")]
if not png_files:
    print("❌ No hay diagramas PNG para dividir en multipágina.")
    exit()

latest_png = max([os.path.join(diagram_dir, f) for f in png_files], key=os.path.getctime)
IMG_FILE = latest_png
OUTPUT_FILE = os.path.join(diagram_dir, f"ERD_COLOR_MULTIPAGE_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf")

img = Image.open(IMG_FILE)
img_width, img_height = img.size

usable_width = PAGE_WIDTH - 2*MARGIN
usable_height = PAGE_HEIGHT - 2*MARGIN
tile_width = usable_width / GRID_COLS
tile_height = usable_height / GRID_ROWS

# Escalado proporcional
scale_x = tile_width / img_width
scale_y = tile_height / img_height
scale = min(scale_x, scale_y) * GRID_COLS

scaled_width = img_width * scale
scaled_height = img_height * scale

tiles_x = math.ceil(scaled_width / usable_width)
tiles_y = math.ceil(scaled_height / usable_height)

c = canvas.Canvas(OUTPUT_FILE, pagesize=letter)

for row in range(tiles_y):
    for col in range(tiles_x):
        x0 = col * usable_width / scale
        y0 = row * usable_height / scale
        x1 = x0 + img_width / tiles_x
        y1 = y0 + img_height / tiles_y

        tile = img.crop((x0, y0, x1, y1))
        temp_tile = f"tile_{row}_{col}.png"
        tile.save(temp_tile)

        c.drawImage(temp_tile, MARGIN, MARGIN, width=usable_width, height=usable_height)
        c.showPage()
        os.remove(temp_tile)

c.save()
print(f"✅ PDF multipágina generado: {OUTPUT_FILE}")
