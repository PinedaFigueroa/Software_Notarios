# archivo: run.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 15
# última actualización: 27 / 07 / 25 hora 21:30
# motivo de la creación: punto de entrada principal para desarrollo y producción
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import create_app

# Creamos la app con la factory
app = create_app()

# Solo para desarrollo
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
