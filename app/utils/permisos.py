# archivo: app/utils/permisos.py
# fecha de creación: 27 / 07 / 25
# cantidad de líneas originales: 30
# última actualización: 27 / 07 / 25 hora 19:45
# motivo de la creación: helper para validar acciones permitidas por rol
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-


"""
Helper de permisos por rol (a nivel de acción).
No reemplaza a los decoradores de acceso a vistas, pero sirve para condicionar
botones/acciones en UI y validar operaciones específicas.

Ejemplo de uso en una vista:
    if not tiene_permiso(current_user, 'gestionar_usuarios'):
        abort(403)

Ejemplo de uso en plantilla Jinja:
    {% if current_user and tiene_permiso(current_user, 'generar_aviso') %}
        <!-- mostrar botón -->
    {% endif %}
"""

from app.models.enums import RolUsuarioEnum



# Permisos definidos por rol
PERMISOS_POR_ROL = {
    RolUsuarioEnum.SUPERADMIN: ["*"],  # acceso total a todo

    RolUsuarioEnum.ADMINISTRADOR: [
        "gestionar_usuarios", "ver_estadisticas", "generar_backup",
        "gestionar_clausulas", "descargar_libreria", "ver_documento", "ver_aviso"
    ],
  
    RolUsuarioEnum.NOTARIO: [
        "crear_documento", "firmar", "asignar_procurador","gestionar_clausulas",
        "asignar_asistente", "ver_documento", "ver_aviso"
    ],

    RolUsuarioEnum.PROCURADOR: [
        "redactar", "ver_documento", "editar_borrador",
        "generar_aviso", "entregar_documento", "ver_aviso"
    ],

    RolUsuarioEnum.ASISTENTE: [
        "imprimir", "generar_aviso", "ver_documento", "ver_aviso"
    ],


}

def tiene_permiso(usuario, accion: str) -> bool:
    """
    Verifica si un usuario tiene permiso para realizar cierta acción
    según su rol en el sistema.

    Args:
        usuario: instancia del modelo Usuario (o similar) con atributo .rol
        accion (str): nombre de la acción a validar

    Returns:
        bool: True si tiene permiso, False en caso contrario.
    """
    
    
    if not usuario or not usuario.rol:
        return False
    acciones = PERMISOS_POR_ROL.get(usuario.rol, [])
    return "*" in acciones or accion in acciones
