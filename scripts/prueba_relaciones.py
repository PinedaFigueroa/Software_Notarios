# archivo: scripts/prueba_relaciones.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 50 aprox.
# última actualización: 27 / 07 / 25 hora 20:05
# motivo de la creación: test de relaciones notario-procurador-asistente según estructura real
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import create_app, db
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum

app = create_app()

with app.app_context():
    print("🧪 Ejecutando prueba de relaciones Notario ↔ Procurador...")

    notario = Usuario.query.filter_by(rol=RolUsuarioEnum.NOTARIO).first()
    if not notario:
        print("⚠️ No hay notarios, creando uno de prueba...")
        notario = Usuario(
            username="notario_test",
            correo="notario@test.com",
            password_hash="test123",
            rol=RolUsuarioEnum.NOTARIO,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=1  # Asegúrate que el bufete 1 exista
        )
        db.session.add(notario)
        db.session.commit()

    print(f"✅ Notario disponible: {notario.username}")

    # Crear 2 procuradores de prueba si no existen
    for i in range(2):
        username = f"procu_test{i+1}"
        if not Usuario.query.filter_by(username=username).first():
            procurador = Usuario(
                username=username,
                correo=f"{username}@test.com",
                password_hash="procu123",
                rol=RolUsuarioEnum.PROCURADOR,
                estado=EstadoUsuarioEnum.ACTIVO,
                bufete_id=notario.bufete_id
            )
            db.session.add(procurador)
            print(f"✅ Procurador creado: {username}")
    db.session.commit()

    # Listar procuradores del bufete
    procuradores = Usuario.query.filter_by(rol=RolUsuarioEnum.PROCURADOR, bufete_id=notario.bufete_id).all()
    print(f"🔎 Procuradores del bufete del notario {notario.username}:")
    for p in procuradores:
        print(f" - {p.username}")

    print("\n📌 NOTA: Para soportar muchos-a-muchos entre notarios y procuradores, se sugiere:")
    print("👉 Crear tabla intermedia notario_procurador_asociacion (notario_id, procurador_id)")
    print("👉 Esto permitiría saber qué procurador trabaja con qué notarios, aunque no pertenezcan al mismo bufete.")
