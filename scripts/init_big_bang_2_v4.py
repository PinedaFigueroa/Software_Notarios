# archivo: scripts/init_big_bang_2_v4.py
# fecha de creación: 29 / 07 / 25
# motivo: Big Bang 2 robusto con tracking y logs de decisiones
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
from datetime import datetime

# Configuración PostgreSQL
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB_NAME = os.getenv("PG_DB_NAME", "software_notarios_dev")

# Carpeta de logs
LOG_DIR = r"C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "big_bang_2_v4.log")

def log_event(msg):
    """Escribe en log y muestra en consola."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(line + "\n")

print("🚀 Inicializador Big Bang 2 v4 — Software Notarios")
print("⚠️  Este proceso eliminará y recreará TODA la base de datos de desarrollo.")
respuesta = input("¿Estás seguro que deseas continuar? (s/n): ").strip().lower()

if respuesta != 's':
    log_event("Operador canceló el proceso en la confirmación inicial. ❌")
    sys.exit(0)

try:
    # 1️⃣ Limpiar migraciones previas
    print("\n--- PASO 1: Limpieza de migraciones ---")
    if os.path.exists("migrations/versions"):
        log_event("Eliminando migraciones previas...")
        for root, dirs, files in os.walk("migrations/versions"):
            for f in files:
                os.remove(os.path.join(root, f))
        log_event("Migraciones limpiadas correctamente. ✅")
    else:
        log_event("Carpeta migrations/versions no existe o ya está vacía. ℹ️")

    # 2️⃣ Detectar si la base existe
    check_db_cmd = [
        "psql",
        "-U", PG_USER,
        "-h", PG_HOST,
        "-p", PG_PORT,
        "-tAc", f"SELECT 1 FROM pg_database WHERE datname='{PG_DB_NAME}';"
    ]
    env = os.environ.copy()
    if PG_PASSWORD:
        env["PGPASSWORD"] = PG_PASSWORD

    result = subprocess.run(check_db_cmd, capture_output=True, text=True, env=env)
    db_exists = result.stdout.strip() == "1"

    if db_exists:
        log_event(f"La base de datos \"{PG_DB_NAME}\" EXISTE.")
        resp = input("¿Deseas eliminarla y recrearla? (s/n): ").strip().lower()
        if resp != 's':
            log_event(f"Operador respondió 'n'. Se aborta el proceso. ❌")
            sys.exit(0)
        else:
            log_event(f"Operador respondió 's'. Se procederá a eliminar y recrear la base.")
            drop_db_cmd = ["psql", "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT,
                           "-c", f"DROP DATABASE {PG_DB_NAME};", "postgres"]
            subprocess.run(drop_db_cmd, check=True, env=env)
            time.sleep(1)
    else:
        log_event(f"La base de datos \"{PG_DB_NAME}\" NO existe.")
        resp = input("¿Deseas crearla y continuar? (s/n): ").strip().lower()
        if resp != 's':
            log_event(f"Operador respondió 'n'. No se crea la base. Se aborta el proceso. ❌")
            sys.exit(0)
        else:
            log_event(f"Operador respondió 's'. Se procederá a crear la base.")

    # 3️⃣ Crear la base de datos UTF8 con template0
    log_event(f"Creando base de datos \"{PG_DB_NAME}\" en UTF8 con template0...")
    create_db_cmd = [
        "psql",
        "-U", PG_USER,
        "-h", PG_HOST,
        "-p", PG_PORT,
        "-c", f"CREATE DATABASE {PG_DB_NAME} WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER {PG_USER};",
        "postgres"
    ]
    result = subprocess.run(create_db_cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        log_event(f"❌ Error al crear DB: {result.stderr.strip()}")
        sys.exit(1)
    log_event("✅ Base de datos creada correctamente.")
    time.sleep(1)

    # 4️⃣ Ejecutar flask db upgrade
    log_event("Aplicando migraciones con flask db upgrade...")
    result = subprocess.run(["flask", "db", "upgrade"], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        log_event(f"❌ Error en upgrade: {result.stderr.strip()}")
        sys.exit(1)
    log_event("✅ Migraciones aplicadas correctamente.")

    # 5️⃣ Ejecutar seed inicial
    log_event("Ejecutando seed inicial...")
    result = subprocess.run([sys.executable, "-m", "scripts.seed_inicial"], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        log_event(f"❌ Error en seed inicial: {result.stderr.strip()}")
        sys.exit(1)
    log_event("✅ Seed inicial completado correctamente.")

    # 6️⃣ Éxito final
    log_event("🎉 Big Bang 2 v4 completado sin errores. La base de datos está lista.")

except Exception as e:
    log_event(f"❌ Excepción inesperada: {str(e)}")
    sys.exit(1)
