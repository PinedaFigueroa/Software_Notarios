# archivo: app/cli.py
# fecha de creación: 14 / 07 / 25 hora 21:50
# ultima actualización: 14 / 07 / 25 hora 23:59
# motivo de la actualizacion: corrección campos que corresponden al notario, no al bufete
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import click
from flask.cli import AppGroup
from app import db
from app.models.core import BufeteJuridico, Notario, UsuarioSistema
from app.models.planes import Plan
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum

cli = AppGroup('seed-cli')

@cli.command('init')
def seed_cli():
    """🌱 Seed inicial: plan Starter, bufete principal, notario y superadmin"""
    print("🌱 Iniciando seed inicial...")

    # 1️⃣ Plan Starter
    plan = Plan.query.filter_by(nombre="Starter").first()
    if not plan:
        plan = Plan(
            nombre="Starter",
            descripcion="Plan inicial con 1 notario, 1 procurador, 1 asistente y 500MB storage",
            max_notarios=1,
            max_procuradores=1,
            max_asistentes=1,
            max_escrituras_mensuales=20,
            max_actas_mensuales=20,
            max_storage_mb=500
        )
        db.session.add(plan)
        db.session.commit()
        print("✅ Plan Starter creado.")
    else:
        print("⚠ Plan Starter ya existe.")

    # 2️⃣ Bufete principal (solo datos del bufete)
    bufete = BufeteJuridico.query.filter_by(nombre_bufete_o_razon_social="PINEDA VON AHN, FIGUEROA Y ASOCIADOS").first()
    if not bufete:
        bufete = BufeteJuridico(
            nombre_bufete_o_razon_social="PINEDA VON AHN, FIGUEROA Y ASOCIADOS",
            nit="CF",
            email="admin@bufete.com",
            app_copyright="© 2025 Pineda von Ahn Figueroa y Asociados / Hubsa  Todos los derechos reservados.",
            nombre_aplicacion="Sistema Notarial Hubsa",
            plan_id=plan.id
        )
        db.session.add(bufete)
        db.session.commit()
        print(f"✅ Bufete creado: {bufete.nombre_bufete_o_razon_social}")
    else:
        print("⚠ Bufete ya existe.")

    # 3️⃣ Notario principal
    notario = Notario.query.filter_by(nombre_completo="Lic. Luis Danilo Pineda von Ahn").first()
    if not notario:
        notario = Notario(
            nombre_completo="Lic. Luis Danilo Pineda von Ahn",
            colegiado="00000",
            direccion="Dirección Inicial",
            telefono="123456",
            bufete_id=bufete.id,
            activo=True
        )
        db.session.add(notario)
        db.session.commit()
        print(f"✅ Notario creado: {notario.nombre_completo}")
    else:
        print("⚠ Notario ya existe.")

    # 4️⃣ Superadmin
    superadmin = UsuarioSistema.query.filter_by(correo="admin@bufete.com").first()
    if not superadmin:
        superadmin = UsuarioSistema(
            nombre_completo="Super Admin",
            correo="admin@bufete.com",
            rol=RolUsuarioEnum.SUPERADMIN,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id,
            activo=True
        )
        db.session.add(superadmin)
        db.session.commit()
        print(f"✅ Usuario superadmin creado: {superadmin.correo}")
    else:
        print("⚠ Superadmin ya existe.")

    print("🎉 Seed inicial completado exitosamente.")
