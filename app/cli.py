# archivo: app/cli.py
# fecha de actualización: 06 / 08 / 25
# motivo de la actualización: corregido uso de "nombre" en vez de "nombre_bufete_o_razon_social"
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import click
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from app import db
from app.models.bufetes import BufeteJuridico
from app.models.usuarios import Usuario, Notario, Procurador, Asistente
from app.models.planes import Plan
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum

cli = AppGroup('seed-cli')

def seed_inicial():
    print("\n🌱 Iniciando seed inicial...")

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
    bufete = BufeteJuridico.query.filter_by(nombre_bufete="PINEDA VON AHN, FIGUEROA Y ASOCIADOS").first()
    if not bufete:
        bufete = BufeteJuridico(
            nombre_bufete="PINEDA VON AHN, FIGUEROA Y ASOCIADOS",
            direccion="5a avenida 15-45 zona 10",
            telefono="2333-4455",
            nit="CF",
            email="admin@bufete.com",
            forma_contacto="Correo institucional",
            plan_id=Plan.query.filter_by(nombre="Profesional").first().id,
            maneja_inventario_timbres_papel = True,
            incluye_libreria_plantillas_inicial= True,
            habilita_auditoria_borrado_logico= True,
            habilita_dashboard_avanzado= True,
            habilita_ayuda_contextual = True,
            habilita_papeleria_digital = False,
        )
        db.session.add(bufete)
        db.session.commit()
        print("✅ Bufete principal creado.")

    # 3️⃣ Notario principal
    if not Notario.query.filter_by(username="notario_pineda").first():
        db.session.add(Notario(
            username="notario_pineda",
            correo="notario@bufete.com",
            password_hash=generate_password_hash("123456"),
            rol=RolUsuarioEnum.NOTARIO,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id,
            numero_colegiado=0
        ))
        db.session.commit()
        print("✅ Notario principal creado.")

    # 4️⃣ Superadmin
    if not Usuario.query.filter_by(username="superadmin").first():
        db.session.add(Usuario(
            username="superadmin",
            correo="admin@bufete.com",
            password_hash=generate_password_hash("123456"),
            rol=RolUsuarioEnum.SUPERADMIN,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id
        ))
        db.session.commit()
        print("✅ Superadmin creado.")

    print("🎉 Seed inicial completado exitosamente.\n")

@cli.command('init')
def seed_cli():
    """🌱 Ejecuta la función seed_inicial con CLI"""
    seed_inicial()
