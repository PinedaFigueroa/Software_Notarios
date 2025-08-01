# archivo: app/dashboard/routes.py
# última actualización: 01 / 08 / 25 hora 20:00
# motivo: agregar variable avisos_pendientes y garantizar render seguro
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from . import dashboard_bp
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum
from app.models.documentos import DocumentoNotarial
from app.models.asociaciones import NotarioProcuradorAsociacion

@dashboard_bp.route("/dashboard")
def dashboard_home():
    # Métricas de usuarios por rol
    usuarios_totales = Usuario.query.count()
    notarios = Usuario.query.filter_by(rol=RolUsuarioEnum.NOTARIO).count()
    procuradores = Usuario.query.filter_by(rol=RolUsuarioEnum.PROCURADOR).count()
    asistentes = Usuario.query.filter_by(rol=RolUsuarioEnum.ASISTENTE).count()
    admins_local = Usuario.query.filter_by(rol=RolUsuarioEnum.ADMIN_LOCAL).count()
    superadmins = Usuario.query.filter_by(rol=RolUsuarioEnum.SUPERADMIN).count()

    # Documentos y asociaciones
    documentos_totales = DocumentoNotarial.query.count()
    asociaciones_activas = NotarioProcuradorAsociacion.query.filter_by(activo=True).count()

    # Placeholder para avisos pendientes (ej: avisos por enviar o vencidos)
    # Luego se reemplazará con query real a la tabla de avisos
    avisos_pendientes = 0

    return render_template(
        "dashboard/dashboard.html",
        usuarios_totales=usuarios_totales,
        notarios=notarios,
        procuradores=procuradores,
        asistentes=asistentes,
        admins_local=admins_local,
        superadmins=superadmins,
        documentos_totales=documentos_totales,
        asociaciones_activas=asociaciones_activas,
        avisos_pendientes=avisos_pendientes
    )
