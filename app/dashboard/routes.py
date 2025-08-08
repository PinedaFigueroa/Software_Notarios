# archivo: app/dashboard/routes.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 37
# última actualización: 07 / 08 / 25 hora 18:00
# motivo de la actualización: corrección de encabezado y lógica por bufete activo
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template
from . import dashboard_bp
from app import db
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum
from app.models.bufetes import BufeteJuridico
from app.models.documentos import DocumentoNotarial
from app.models.asociaciones import NotarioProcuradorAsociacion

@dashboard_bp.route("/dashboard")
def mostrar_dashboard():
    # Tomar el primer bufete creado (puedes ajustar esto por sesión de usuario en el futuro)
    bufete = BufeteJuridico.query.order_by(BufeteJuridico.id.asc()).first()

    usuarios_totales = Usuario.query.filter_by(bufete_id=bufete.id).count()
    notarios = Usuario.query.filter_by(bufete_id=bufete.id, rol=RolUsuarioEnum.NOTARIO).count()
    procuradores = Usuario.query.filter_by(bufete_id=bufete.id, rol=RolUsuarioEnum.PROCURADOR).count()
    asistentes = Usuario.query.filter_by(bufete_id=bufete.id, rol=RolUsuarioEnum.ASISTENTE).count()
    admins_local = Usuario.query.filter_by(bufete_id=bufete.id, rol=RolUsuarioEnum.ADMINISTRADOR).count()
    superadmins = Usuario.query.filter_by(bufete_id=bufete.id, rol=RolUsuarioEnum.SUPERADMIN).count()

    documentos_totales = DocumentoNotarial.query.filter_by(bufete_id=bufete.id).count()
    asociaciones_activas = NotarioProcuradorAsociacion.query.filter_by(activo=True, bufete_id=bufete.id).count()

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
