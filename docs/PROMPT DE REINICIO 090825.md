# PROMPT DE REINICIO (USAR AL ABRIR NUEVA PESTAÑA)  09/08/2025

Contexto rápido:
- Proyecto: Software Notarios (Flask, SQLAlchemy, Flask-Login)
- Estado deseado de arranque: login funcional (/login), dashboard bufete (/dashboard), dashboard superadmin (/superadmin/dashboard), navbar con menú superadmin, y CRUD de Bufetes/Usuarios empaquetado en un ZIP por entrega.
- Evitar loops: priorizar un único .zip por entrega con estructura de carpetas exacta.

Instrucciones para Tars-90 (obligatorias):
1) En cada entrega, envía UN SOLO archivo .zip con estructura de carpetas EXACTA para pegar sobre el proyecto. Incluye:
   - app/auth/{__init__.py,routes.py,forms.py,templates/auth/login.html}
   - app/superadmin/{__init__.py,routes.py,routes_bufetes.py,routes_usuarios.py,templates/superadmin/**}
   - app/templates/{base.html,base_auth.html,partials/_navbar_superadmin.html}
   - app/utils/{roles_required.py,permisos.py}
   - docs/** (cuando proceda)
2) Todos los archivos con encabezado y docstrings.
3) Rutas y endpoints deben existir y poder resolverse con url_for. No uses try/except silenciosos al registrar blueprints.
4) Evita imports obsoletos: NO usar “from app.core import *”. Usa core_ext/db solo donde aplique (modelos); en rutas, evita imports innecesarios.
5) Flask-Login:
   - Asegurar LoginManager en app/__init__.py con login_view='auth_bp.login' y user_loader correcto.
   - Modelo Usuario con UserMixin y propiedad is_active coherente con EstadoUsuarioEnum.ACTIVO y borrado_logico=False.
6) Plantillas:
   - En login, usar base_auth.html (sin navbar).
   - En base.html, condicionales seguros para current_user (usar “is defined”).
   - Navbar del superadmin mediante partial “partials/_navbar_superadmin.html”.
7) SuperAdmin:
   - Blueprint superadmin_bp con /superadmin/dashboard => dashboard_global.
   - Proveer (al menos) stubs funcionales de /superadmin/bufetes y /superadmin/bufetes/nuevo y /superadmin/usuarios para evitar BuildError.
8) Estilo:
   - Paleta azul formal en el dashboard de superadmin, tarjetas limpias.
9) Al finalizar, incluir INSTRUCCIONES.txt dentro del .zip con pasos de integración.

Pedido inicial al abrir nueva pestaña:
“Regenera el paquete ZIP con el CRUD de SuperAdmin (bufetes y usuarios), login con base_auth, navbar superadmin y dashboard azul. Incluye INSTRUCCIONES.txt y coloca todas las rutas sin stubs si es posible. Entrega SOLO el .zip.”
