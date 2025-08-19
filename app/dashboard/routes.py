# archivo: app/dashboard/routes.py
# fecha de actualización: 29 / 07 / 25
# motivo: mostrar métricas reales en dashboard con cards Bootstrap
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from . import dashboard_bp
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum
from app.models.documentos import DocumentoNotarial
from app.models.asociaciones import NotarioProcuradorAsociacion

@dashboard_bp.route("/dashboard")
def mostrar_dashboard():
    # Métricas de usuarios por rol
    usuarios_totales = Usuario.query.count()
    notarios = Usuario.query.filter_by(rol=RolUsuarioEnum.NOTARIO).count()
    procuradores = Usuario.query.filter_by(rol=RolUsuarioEnum.PROCURADOR).count()
    asistentes = Usuario.query.filter_by(rol=RolUsuarioEnum.ASISTENTE).count()
    admins_local = Usuario.query.filter_by(rol=RolUsuarioEnum.ADMINISTRADOR).count()
    superadmins = Usuario.query.filter_by(rol=RolUsuarioEnum.SUPERADMIN).count()

    # Documentos y asociaciones
    documentos_totales = DocumentoNotarial.query.count()
    asociaciones_activas = NotarioProcuradorAsociacion.query.filter_by(activo=True).count()

    return render_template(
        "dashboard/dashboard.html",
        usuarios_totales=usuarios_totales,
        notarios=notarios,
        procuradores=procuradores,
        asistentes=asistentes,
        admins_local=admins_local,
        superadmins=superadmins,
        documentos_totales=documentos_totales,
        asociaciones_activas=asociaciones_activas
    )
