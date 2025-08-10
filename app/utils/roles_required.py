# archivo: app/utils/roles_required.py
# fecha de creación: 07 / 08 / 25
# cantidad de líneas originales: 60
# última actualización: 09 / 08 / 25 hora 18:55
# motivo de la actualización: Decoradores robustos para control de acceso por rol (con alias)
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Decoradores para restringir vistas según roles de usuario.

Uso típico:
    from flask_login import login_required
    from app.utils.roles_required import rol_required

    @bp.route('/ruta-protegida')
    @login_required
    @rol_required(['SUPERADMIN', 'ADMINISTRADOR'])
    def vista():
        ...

Detalles:
- Soporta listas/tuplas de roles en formato string (e.g. 'SUPERADMIN')
  o instancias de RolUsuarioEnum (e.g. RolUsuarioEnum.SUPERADMIN).
- Hace comparaciones por `current_user.rol.name`.
- Si el usuario NO está autenticado, deja que `@login_required` lo maneje.
- Si el rol del usuario no califica, lanza 403.
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from app.models.enums import RolUsuarioEnum


def _to_role_names(roles):
    """Normaliza lista de roles a una lista de strings con los nombres del enum."""
    names = set()
    if not roles:
        return names
    for r in roles:
        if isinstance(r, RolUsuarioEnum):
            names.add(r.name)
        elif isinstance(r, str):
            names.add(r.upper().strip())
        else:
            # Ignorar tipos inesperados, o podríamos lanzar ValueError
            continue
    return names


def rol_required(roles):
    """
    Restringe el acceso a usuarios cuyo rol esté en `roles`.

    Args:
        roles (Iterable[str|RolUsuarioEnum]): roles permitidos.
    """
    allowed = _to_role_names(roles)

    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            # current_user puede no existir en ciertos contextos (plantillas estáticas, etc.)
            if not hasattr(current_user, "is_authenticated") or not current_user.is_authenticated:
                # Deja que @login_required se encargue de redirigir (si está aplicado)
                abort(401)

            # Si el usuario no tiene rol (dato inconsistente)
            if not getattr(current_user, "rol", None):
                abort(403)

            user_role_name = getattr(getattr(current_user, "rol", None), "name", None)
            if user_role_name is None or user_role_name not in allowed:
                abort(403)

            return f(*args, **kwargs)
        return decorated_view
    return wrapper


# Alias para quien prefiera plural:
roles_required = rol_required
