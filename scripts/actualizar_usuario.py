# archivo: scripts/actualizar_usuario.py
# fecha de creación: 08 / 08 / 25
# cantidad de líneas originales: 43
# última actualización: 08 / 08 / 25 hora 14:00
# motivo de la creación: Script general para actualizar datos de cualquier usuario
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Script interactivo para actualizar información de usuarios existentes en la base de datos.
Permite modificar nombre, apellido, correo, teléfono u otros campos de forma dinámica.
"""

# tars siempre olvida poner estas 3 lineas
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import click
from app import create_app
from flask import Flask
from app.core_ext import db
from app.models.usuarios import Usuario

app = create_app()
app.app_context().push()

@click.command()
@click.option('--username', prompt='Username del usuario a modificar', help='Username actual del usuario')
def actualizar_usuario(username):
    usuario = Usuario.query.filter_by(username=username).first()
    if not usuario:
        click.echo("❌ Usuario con username '{}' no encontrado.".format(username))
        return

    click.echo("🔍 Usuario encontrado: {} ({})".format(usuario.username, usuario.rol))

    campos_modificables = ['nombres', 'apellidos', 'correo', 'telefono', 'direccion_laboral', 'preferencia_contacto_red_social']
    for campo in campos_modificables:
        valor_actual = getattr(usuario, campo)
        nuevo_valor = click.prompt("Nuevo valor para '{}' (actual: {})".format(campo, valor_actual), default=valor_actual, show_default=False)
        setattr(usuario, campo, nuevo_valor)

    db.session.commit()
    click.echo("✅ Usuario actualizado correctamente.")

if __name__ == '__main__':
    actualizar_usuario()
