# archivo: app/utils/permisos.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 30
# última actualización: 27 / 07 / 25 hora 19:45
# motivo de la creación: helper para validar acciones permitidas por rol
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app.models.enums import RolUsuarioEnum

# Permisos definidos por rol
PERMISOS_POR_ROL = {
    RolUsuarioEnum.SUPERADMIN: ["*"],  # acceso total a todo

    RolUsuarioEnum.NOTARIO: [
        "crear_documento", "firmar", "asignar_procurador",
        "asignar_asistente", "ver_documento", "ver_aviso"
    ],

    RolUsuarioEnum.PROCURADOR: [
        "redactar", "ver_documento", "editar_borrador",
        "generar_aviso", "entregar_documento", "ver_aviso"
    ],

    RolUsuarioEnum.ASISTENTE: [
        "imprimir", "generar_aviso", "ver_documento", "ver_aviso"
    ],

    RolUsuarioEnum.ADMIN_LOCAL: [
        "gestionar_usuarios", "ver_estadisticas", "generar_backup",
        "gestionar_clausulas", "descargar_libreria"
    ],
}

def tiene_permiso(usuario, accion):
    """
    Verifica si un usuario tiene permiso para realizar cierta acción
    según su rol en el sistema.
    """
    if not usuario or not usuario.rol:
        return False
    acciones = PERMISOS_POR_ROL.get(usuario.rol, [])
    return "*" in acciones or accion in acciones
