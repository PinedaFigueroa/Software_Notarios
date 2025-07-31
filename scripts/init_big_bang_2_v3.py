# archivo: scripts/init_big_bang_2_v3.py
# fecha de creación: 29 / 07 / 25
# motivo: Big Bang 2 completo, versión robusta con tracking y logs
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
from datetime import datetime

# Configuración de PostgreSQL
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB_NAME = os.getenv("PG_DB_NAME", "software_notarios_dev")

# Carpeta de logs
LOG_DIR = r"C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "big_bang_2_v3_error.log")

print("🚀 Inicializador Big Bang 2 v3 — Software Notarios")
print("⚠️  Este proceso eliminará y recreará TODA la base de datos de desarrollo.")
respuesta = input("¿Estás seguro que deseas continuar? (s/n): ").strip().lower()

if respuesta != 's':
    print("❌ Proceso cancelado por el usuario.")
    sys.exit(0)

try:
    # 1️⃣ Limpiar migraciones previas
    print("\n--- PASO 1: Limpieza de migraciones ---")
    if os.path.exists("migrations/versions"):
        print("🗑️  Eliminando archivos de migraciones previas...")
        for root, dirs, files in os.walk("migrations/versions"):
            for f in files:
                os.remove(os.path.join(root, f))
        print("✅ Migraciones limpiadas.")
    else:
        print("ℹ️  Carpeta migrations/versions no existe o ya está vacía.")

    # 2️⃣ Crear la base de datos UTF8 con template0
    print("\n--- PASO 2: Creación de base de datos UTF8 con template0 ---")
    create_db_cmd = [
        "psql",
        "-U", PG_USER,
        "-h", PG_HOST,
        "-p", PG_PORT,
        "-c", f"CREATE DATABASE {PG_DB_NAME} WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER {PG_USER};",
        "postgres"
    ]
    env = os.environ.copy()
    if PG_PASSWORD:
        env["PGPASSWORD"] = PG_PASSWORD

    result = subprocess.run(create_db_cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] Error al crear DB:\n{result.stderr}\n")
        print(f"❌ ERROR al crear DB. Revisa {LOG_FILE}")
        sys.exit(1)
    print("✅ Base de datos creada correctamente.")
    time.sleep(1)

    # 3️⃣ Ejecutar upgrade
    print("\n--- PASO 3: Aplicando migraciones (flask db upgrade) ---")
    result = subprocess.run(["flask", "db", "upgrade"], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] Error en upgrade:\n{result.stderr}\n")
        print(f"❌ Error durante upgrade. Revisa {LOG_FILE}")
        sys.exit(1)
    print("✅ Migraciones aplicadas correctamente.")

    # 4️⃣ Ejecutar seed inicial
    print("\n--- PASO 4: Ejecutando seed inicial ---")
    result = subprocess.run([sys.executable, "-m", "scripts.seed_inicial"], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] Error en seed inicial:\n{result.stderr}\n")
        print(f"❌ Error durante seed inicial. Revisa {LOG_FILE}")
        sys.exit(1)
    print("✅ Seed inicial completado correctamente.")

    # 5️⃣ Éxito
    print("\n🎉 Big Bang 2 v3 completado sin errores. La base de datos está lista.")

except Exception as e:
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] Excepción inesperada: {str(e)}\n")
    print(f"❌ Excepción inesperada. Revisa {LOG_FILE}")
    sys.exit(1)
