# archivo: app/cli.py
# fecha de actualización: 26 / 07 / 25
# motivo: agregar numero_colegiado=0 al notario principal y asegurar integridad con modelos
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import click
from flask.cli import AppGroup
from app.extensions import db
from app.models.usuarios import BufeteJuridico, Notario, Usuario
from app.models.planes import Plan
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum

cli = AppGroup('seed-cli')

def seed_inicial():
    print("🌱 Iniciando seed inicial...")

    # 1️⃣ Planes base
    planes = [
        ("Demo", "Acceso limitado de prueba", 1, 1, 1, 5, 50, 0.0),
        ("Profesional", "Para bufetes pequeños o en crecimiento", 2, 3, 2, 100, 500, 250.0),
        ("Ilimitado", "Sin límites técnicos", 999, 999, 999, 99999, 100000, 1250.0),
    ]

    for nombre, descripcion, n, p, a, doc, mb, precio in planes:
        if not Plan.query.filter_by(nombre=nombre).first():
            db.session.add(Plan(
                nombre=nombre,
                descripcion=descripcion,
                max_notarios=n,
                max_procuradores=p,
                max_asistentes=a,
                max_documentos=doc,
                storage_mb=mb,
                precio_mensual=precio
            ))
    db.session.commit()
    print("✅ Planes base creados.")

    # 2️⃣ Bufete principal
    bufete = BufeteJuridico.query.filter_by(nombre_bufete_o_razon_social="PINEDA VON AHN, FIGUEROA Y ASOCIADOS").first()
    if not bufete:
        bufete = BufeteJuridico(
            nombre_bufete_o_razon_social="PINEDA VON AHN, FIGUEROA Y ASOCIADOS",
            nit="CF",
            email="admin@bufete.com",
            app_copyright="© 2025 Pineda von Ahn Figueroa y Asociados / Hubsa  Todos los derechos reservados.",
            nombre_aplicacion="Sistema Notarial Hubsa",
            plan_id=Plan.query.filter_by(nombre="Profesional").first().id
        )
        db.session.add(bufete)
        db.session.commit()
        print("✅ Bufete principal creado.")

    # 3️⃣ Notario principal
    if not Notario.query.filter_by(username="notario_pineda").first():
        db.session.add(Notario(
            username="notario_pineda",
            correo="notario@bufete.com",
            password_hash="hashed_password",  # reemplazar por hash real
            rol=RolUsuarioEnum.NOTARIO,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id,
            numero_colegiado=0
        ))
        db.session.commit()
        print("✅ Notario principal creado.")

    # 4️⃣ Superadmin
    if not Usuario.query.filter_by(username="admin").first():
        db.session.add(Usuario(
            username="admin",
            correo="admin@bufete.com",
            password_hash="admin123",  # reemplazar por hash real
            rol=RolUsuarioEnum.SUPERADMIN,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id
        ))
        db.session.commit()
        print("✅ Superadmin creado.")

    print("🎉 Seed inicial completado.")

@cli.command('init')
def seed_cli():
    """🌱 Ejecuta la función seed_inicial con CLI"""
    seed_inicial()
