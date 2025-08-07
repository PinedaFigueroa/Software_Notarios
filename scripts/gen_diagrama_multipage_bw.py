# archivo: scripts/gen_diagrama_multipage_bw.py
# fecha de creación: 05 / 08 / 25
# cantidad de lineas originales: 120 aprox.
# última actualización: 05 / 08 / 25 hora 17:30
# motivo de la actualización: Multipágina 4x4 funcional con encabezados y pies de página
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Genera un PDF multipágina en blanco y negro del diagrama ER.

- Carga la imagen completa del diagrama
- La divide en 4x4 páginas (16)
- Añade encabezados y pies de página
- Borra tiles temporales
"""

import os
import math
import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# ------------------- CONFIGURACIÓN -------------------
IMG_FILE = r"db_docs\Diagramas\ERD_COLOR_20250805_1653.png"  # Cambia según tu diagrama generado
OUTPUT_FILE = r"db_docs\Diagramas\ERD_MULTIPAGE_BW.pdf"

GRID_ROWS = 4
GRID_COLS = 4
MARGIN = 2.5 * cm
PAGE_WIDTH, PAGE_HEIGHT = letter

# ------------------- CARGAR IMAGEN -------------------
if not os.path.exists(IMG_FILE):
    raise FileNotFoundError(f"No se encuentra la imagen del diagrama: {IMG_FILE}")

img = Image.open(IMG_FILE).convert("L")  # Convertir a blanco y negro
img_width, img_height = img.size

usable_width = PAGE_WIDTH - 2*MARGIN
usable_height = PAGE_HEIGHT - 2*MARGIN

tile_width = img_width / GRID_COLS
tile_height = img_height / GRID_ROWS

total_pages = GRID_ROWS * GRID_COLS
c = canvas.Canvas(OUTPUT_FILE, pagesize=letter)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# ------------------- GENERAR PÁGINAS -------------------
page_num = 1
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        # Coordenadas del recorte
        x0 = col * tile_width
        y0 = img_height - (row+1) * tile_height
        x1 = x0 + tile_width
        y1 = y0 + tile_height

        tile = img.crop((x0, y0, x1, y1))
        temp_tile = f"tile_bw_{row}_{col}.png"
        tile.save(temp_tile)

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 1*cm, "Base de Datos Software Notarios")

        # Pie de página
        c.setFont("Helvetica", 9)
        c.drawCentredString(PAGE_WIDTH/2, 1*cm,
                            f"Página {page_num} de {total_pages} - Generado el {now}")

        # Imagen recortada
        c.drawImage(temp_tile, MARGIN, MARGIN,
                    width=usable_width, height=usable_height)

        c.showPage()
        page_num += 1
        os.remove(temp_tile)  # limpiar tile

c.save()
print(f"✅ PDF multipágina en blanco y negro generado: {OUTPUT_FILE}")
