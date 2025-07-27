# archivo: scripts/init_dev_db.py
# fecha de creación: 26 / 07 / 25
# cantidad de lineas originales: 40 aprox.
# última actualización: 26 / 07 / 25 hora 22:10
# motivo de la actualización: llamada directa a seed_inicial() sin usar click context
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path

from app import create_app, db
from app.cli import seed_inicial

LOG_PATH = Path("C:/Users/Usuario/Mi unidad/Software_Notarios/errores_bdd_flask/init_error.log")

def log_error(msg):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def confirm():
    try:
        respuesta = input("⚠️ ¿Estás seguro que deseas reiniciar TODA la base de datos? (s/n): ").strip().lower()
        return respuesta == "s"
    except Exception as e:
        log_error(f"Error leyendo confirmación: {e}")
        return False

def init_dev_db():
    app = create_app()
    with app.app_context():
        try:
            print("🔄 Borrando y recreando base de datos...")
            db.drop_all()
            db.create_all()
            print("✅ Tablas recreadas exitosamente.")
        except Exception as e:
            log_error(f"Error al recrear tablas: {e}")
            print("❌ Error al recrear tablas. Revisa el archivo de log.")
            return

        try:
            print("🌱 Ejecutando seed inicial (planes, bufete, usuarios)...")
            seed_inicial()
            print("🎉 Base de datos inicializada correctamente.")
        except Exception as e:
            log_error(f"Error ejecutando seed: {e}")
            print("❌ Error al ejecutar seed. Revisa el archivo de log.")

if __name__ == '__main__':
    print("🚧 Inicializador de entorno de desarrollo SWNotarios")
    if confirm():
        init_dev_db()
    else:
        print("❎ Operación cancelada por el usuario.")
