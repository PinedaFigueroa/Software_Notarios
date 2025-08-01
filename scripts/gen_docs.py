# archivo: scripts/gen_docs.py
# última actualización: 01 / 08 / 25 hora 21:15
# motivo: Generación automática de documentación Sphinx con inclusión de .md diarios
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

PROJECT_DIR = r"C:\Users\Usuario\Mi unidad\Software_Notarios"
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")
BUILD_DIR = os.path.join(DOCS_DIR, "_build", "html")
MOD_DIR = os.path.join(DOCS_DIR, "modulos")
INDEX_FILE = os.path.join(DOCS_DIR, "index.rst")

def clean_old_rst():
    """Elimina .rst huérfanos de versiones antiguas."""
    for file in os.listdir(MOD_DIR):
        if "_v" in file or "copia" in file.lower():
            os.remove(os.path.join(MOD_DIR, file))
            print(f"🧹 Eliminado: {file}")

def update_index_rst():
    """Genera un index.rst incluyendo todos los .md relevantes automáticamente."""
    header = """Software Notarios Documentation
================================

.. toctree::
   :maxdepth: 2
   :caption: Contenido del Proyecto

"""
    lines = [header]
    # 1️⃣ Incluir todos los archivos Markdown
    for file in sorted(os.listdir(DOCS_DIR)):
        if file.endswith(".md"):
            lines.append(f"   {file}\n")

 # 2️⃣ Incluir automáticamente RST de módulos y source
    lines.append("\n   modulos/*\n")
    lines.append("   source/*\n")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"📝 index.rst actualizado con {len(lines)-1} archivos Markdown")

def generate_docs():
    """Genera documentación automática para app y scripts."""
    os.chdir(DOCS_DIR)
    print("📚 Generando documentación Sphinx...")

    # 1️⃣ Limpieza de .rst viejos
    clean_old_rst()

    # 2️⃣ Actualizar index.rst con .md del día
    update_index_rst()

    # 3️⃣ Autodoc para módulos
    subprocess.run(["sphinx-apidoc", "-o", "modulos", "../app"], shell=True)
    subprocess.run(["sphinx-apidoc", "-o", "modulos", "../scripts"], shell=True)

    # 4️⃣ Compilar HTML
    subprocess.run(["make.bat", "html"], shell=True)
    print(f"✅ Documentación generada en {BUILD_DIR}\\index.html")

if __name__ == "__main__":
    generate_docs()
