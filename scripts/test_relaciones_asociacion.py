# archivo: scripts/test_relaciones_asociacion.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: ~40
# última actualización: 27 / 07 / 25 hora 20:55
# motivo de la creación: prueba funcional de tabla notario_procurador_asociacion
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models.asociaciones import NotarioProcuradorAsociacion
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum

app = create_app()

with app.app_context():
    print("🧪 Test de asociación Notario ↔ Procurador")

    notario = Usuario.query.filter_by(rol=RolUsuarioEnum.NOTARIO).first()
    procurador = Usuario.query.filter_by(rol=RolUsuarioEnum.PROCURADOR).first()

    if not notario or not procurador:
        print("⚠️ No se encontraron notario y procurador válidos. Ejecuta primero 'prueba_relaciones.py'")
    else:
        # Verificar si ya existe
        existente = NotarioProcuradorAsociacion.query.filter_by(
            notario_id=notario.id, procurador_id=procurador.id, activo=True
        ).first()

        if existente:
            print(f"ℹ️ Ya existe asociación activa entre {notario.username} y {procurador.username}.")
        else:
            nueva = NotarioProcuradorAsociacion(
                notario_id=notario.id,
                procurador_id=procurador.id,
                bufete_id=notario.bufete_id
            )
            db.session.add(nueva)
            db.session.commit()
            print(f"✅ Asociación creada entre {notario.username} y {procurador.username}.")

        # Mostrar asociaciones activas
        print("\n📋 Asociaciones activas en la tabla:")
        asociaciones = NotarioProcuradorAsociacion.query.filter_by(activo=True).all()
        for a in asociaciones:
            print(f" - Notario ID: {a.notario_id} ↔ Procurador ID: {a.procurador_id}")
