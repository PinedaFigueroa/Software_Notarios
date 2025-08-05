# archivo: scripts/gen_docs.py
# última actualización: 01 / 08 / 25 hora 22:00
# motivo: Generación automática de documentación Sphinx con inclusión de .md, modulos/* y source/*
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import subprocess

# Rutas principales
PROJECT_DIR = r"C:\Users\Usuario\Mi unidad\Software_Notarios"
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")
BUILD_DIR = os.path.join(DOCS_DIR, "_build", "html")
MOD_DIR = os.path.join(DOCS_DIR, "modulos")
SRC_DIR = os.path.join(DOCS_DIR, "source")
INDEX_FILE = os.path.join(DOCS_DIR, "index.rst")

def clean_old_rst():
    """Elimina .rst huérfanos de versiones antiguas."""
    for folder in [MOD_DIR, SRC_DIR]:
        for file in os.listdir(folder):
            if "_v" in file or "copia" in file.lower():
                os.remove(os.path.join(folder, file))
                print(f"🧹 Eliminado: {file}")

def update_index_rst():
    """Genera un index.rst incluyendo .md, modulos/* y source/* automáticamente."""
    header = """Software Notarios Documentation
================================

.. toctree::
   :maxdepth: 2
   :caption: Contenido del Proyecto

"""
    lines = [header]

    # 1️⃣ Incluir todos los archivos Markdown de docs/
    for file in sorted(os.listdir(DOCS_DIR)):
        if file.endswith(".md"):
            lines.append(f"   {file}\n")

    # 2️⃣ Incluir automáticamente RST de modulos/ y source/
    lines.append("\n   modulos/*\n")
    lines.append("   source/*\n")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"📝 index.rst actualizado con {len(lines)-1} entradas (incluye modulos/* y source/*)")

def generate_docs():
    """Genera documentación automática para app y scripts."""
    os.chdir(DOCS_DIR)
    print("📚 Generando documentación Sphinx...")

    # 1️⃣ Limpieza de .rst viejos
    clean_old_rst()

    # 2️⃣ Actualizar index.rst
    update_index_rst()

    # 3️⃣ Generar RST para módulos de app/ y scripts/
    subprocess.run(["sphinx-apidoc", "-o", "modulos", "../app"], shell=True)
    subprocess.run(["sphinx-apidoc", "-o", "modulos", "../scripts"], shell=True)

    # 4️⃣ Compilar HTML
    subprocess.run(["make.bat", "html"], shell=True)
    print(f"✅ Documentación generada en {BUILD_DIR}\\index.html")

if __name__ == "__main__":
    generate_docs()
