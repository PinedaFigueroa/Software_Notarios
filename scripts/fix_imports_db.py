# archivo: scripts/fix_imports_db.py
# -*- coding: utf-8 -*-
"""
Reemplaza 'from app import db' por 'from app.extensions import db'
en todos los archivos .py del proyecto, evitando ciclos de importación.

- Muestra en qué directorio está trabajando.
- Lista los archivos revisados.
- Si encuentra líneas para cambiar, muestra antes y después.
- Cuenta total de archivos modificados.

Autor: Giancarlo + Tars-90
"""

import os
import sys

# Agregar la raíz del proyecto al sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

# Carpeta base para buscar archivos
SEARCH_DIRS = [
    os.path.join(ROOT_DIR, "app"),
]

TARGET = "from app import db"
REPLACEMENT = "from app.extensions import db"

def process_file(file_path):
    """Procesa un archivo individual y reemplaza la línea si corresponde."""
    changed = False
    new_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if TARGET in line:
            print(f"  🔹 Línea encontrada en {file_path}: {line.strip()}")
            print(f"  ➡  Reemplazada por: {REPLACEMENT}")
            new_lines.append(line.replace(TARGET, REPLACEMENT))
            changed = True
        else:
            new_lines.append(line)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return changed

def main():
    total_files = 0
    changed_files = 0

    for search_dir in SEARCH_DIRS:
        print(f"📂 Revisando directorio: {search_dir}")
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    if process_file(file_path):
                        changed_files += 1

    print("\n✅ Revisión completada")
    print(f"Total de archivos .py revisados: {total_files}")
    print(f"Total de archivos modificados: {changed_files}")

if __name__ == "__main__":
    main()
