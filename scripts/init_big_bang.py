# archivo: scripts/init_big_bang.py
# fecha de creación: 29 / 07 / 25
# última actualización: 31 / 07 / 25 hora 18:15
# motivo: encapsulación en main() para evitar ejecución al importar
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Inicializador Big Bang definitivo para Software Notarios.
- Híbrido Windows/Linux
- Limpia migraciones, recrea DB y aplica seed inicial
- Genera log por ejecución con timestamp
"""

import os
import sys
import subprocess
import platform
import time
from datetime import datetime

LOG_DIR = r"C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"big_bang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def log_event(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(line + "\n")

def main():
    IS_WINDOWS = platform.system().lower() == "windows"
    CURRENT_PATH = os.getcwd()
    ROUTE_HAS_SPACES = " " in CURRENT_PATH

    log_event("🚀 Inicializador Big Bang — Software Notarios")

    # --- Ejecución .BAT si es Windows con espacios ---
    if IS_WINDOWS and ROUTE_HAS_SPACES:
        log_event("⚠️  Windows detectado con ruta que contiene espacios.")
        log_event("💡 Ejecutando el .bat oficial para evitar errores con psycopg2.")
        
        bat_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "init_dev_db.bat"))
        if not os.path.exists(bat_path):
            log_event(f"❌ No se encontró {bat_path}. Coloca el .bat en la raíz del proyecto.")
            sys.exit(1)

        result = subprocess.run(["cmd.exe", "/c", bat_path], shell=True)
        sys.exit(result.returncode)

    # --- Configuración de DB ---
    PG_USER = os.getenv("PG_USER", "postgres")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "")
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_DB_NAME = os.getenv("PG_DB_NAME", "software_notarios")

    env = os.environ.copy()
    if PG_PASSWORD:
        env["PGPASSWORD"] = PG_PASSWORD

    log_event("⚙️ Ejecutando Big Bang en modo Python...")

    try:
        # 1️⃣ Limpieza de migraciones
        log_event("--- PASO 1: Limpieza de migraciones ---")
        if os.path.exists("migrations/versions"):
            for root, dirs, files in os.walk("migrations/versions"):
                for f in files:
                    os.remove(os.path.join(root, f))
            log_event("✅ Migraciones limpiadas.")
        else:
            log_event("ℹ️ Carpeta migrations/versions no existe o ya está vacía.")

        # 2️⃣ Detección y eliminación de DB previa
        check_db_cmd = [
            "psql", "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT,
            "-tAc", f"SELECT 1 FROM pg_database WHERE datname='{PG_DB_NAME}';"
        ]
        result = subprocess.run(check_db_cmd, capture_output=True, text=True, env=env)
        db_exists = result.stdout.strip() == "1"

        if db_exists:
            log_event(f"La base de datos \"{PG_DB_NAME}\" EXISTE.")
            resp = input("¿Deseas eliminarla y recrearla? (s/n): ").strip().lower()
            if resp != 's':
                log_event("Operador canceló el proceso. ❌")
                sys.exit(0)
            drop_db_cmd = [
                "psql", "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT,
                "-c", f"DROP DATABASE {PG_DB_NAME};", "postgres"
            ]
            subprocess.run(drop_db_cmd, check=True, env=env)
            time.sleep(1)
        else:
            log_event(f"La base de datos \"{PG_DB_NAME}\" NO existe.")
            resp = input("¿Deseas crearla y continuar? (s/n): ").strip().lower()
            if resp != 's':
                log_event("Operador canceló la creación. ❌")
                sys.exit(0)

        # 3️⃣ Crear DB UTF8 con template0
        log_event(f"Creando base de datos \"{PG_DB_NAME}\" UTF8 con template0...")
        create_db_cmd = [
            "psql", "-U", PG_USER, "-h", PG_HOST, "-p", PG_PORT,
            "-c", f"CREATE DATABASE {PG_DB_NAME} WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER {PG_USER};",
            "postgres"
        ]
        result = subprocess.run(create_db_cmd, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            log_event(f"❌ Error al crear DB: {result.stderr.strip()}")
            sys.exit(1)
        log_event("✅ Base creada correctamente.")
        time.sleep(1)

        # 4️⃣ Aplicar migraciones
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

        log_event("🎉 Big Bang completado sin errores.")

    except Exception as e:
        log_event(f"❌ Excepción inesperada: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
