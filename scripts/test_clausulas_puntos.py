# archivo: scripts/test_clausulas_puntos.py
# fecha de creación: 29 / 07 / 25
# motivo: prueba de inserción de cláusulas/puntos en DB
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models.clausulas_puntos import ClausulasPuntos
from app.models.enums import TipoClausulaEnum, TipoAplicacionClausulaEnum

app = create_app()

with app.app_context():
    print("🧪 Insertando ejemplos en clausulas_puntos...")

    ejemplos = [
        ClausulasPuntos(
            nombre="PRIMERO: REQUERIMIENTO",
            contenido="El compareciente declara su requerimiento de ...",
            tipo=TipoClausulaEnum.OBLIGATORIA,
            aplicacion=TipoAplicacionClausulaEnum.ACTA
        ),
        ClausulasPuntos(
            nombre="SEGUNDO: DECLARACIÓN JURADA",
            contenido="El compareciente manifiesta bajo juramento ...",
            tipo=TipoClausulaEnum.GENERAL,
            aplicacion=TipoAplicacionClausulaEnum.ACTA
        )
    ]

    db.session.add_all(ejemplos)
    db.session.commit()

    print("✅ Ejemplos insertados correctamente.")
