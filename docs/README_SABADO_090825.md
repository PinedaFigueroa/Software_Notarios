# README — Sábado 09/08/2025 (bitácora rápida)

## Resumen del día
Día complejo con varias regresiones y correcciones. Se logró cerrar el día con:
- **Login** funcional (Flask-Login) y **dashboard de SuperAdmin** accesible.
- **Menú de SuperAdmin** en el navbar y **stubs** para Bufetes/Usuarios (para que no rompan rutas).
- **Paleta azul formal** aplicada al dashboard de SuperAdmin.
- **Base de autenticación** (`base_auth.html`) para ocultar navbar en la página de login.

## Problemas encontrados y soluciones
1. `current_user` undefined en plantillas  
   - Causa: LoginManager no inicializado/registro incompleto de auth.  
   - Solución: Inicializar `login_manager.init_app(app)`, definir `user_loader`, y usar checks seguros en `base.html` (`current_user is defined`).

2. Error `is_active` y `get_id` en `Usuario`  
   - Causa: El modelo no tenía `UserMixin` ni `is_active`.  
   - Solución: Heredar de `UserMixin`, implementar `is_active` conforme a `EstadoUsuarioEnum.ACTIVO` y `borrado_logico=False`.

3. `BuildError` con endpoints (e.g., `superadmin_bp.dashboard_global`, `superadmin_bp.listar_bufetes`, `superadmin_bp.crear_bufete`)  
   - Causa: Blueprints/rutas no registradas o endpoints inexistentes.  
   - Solución: Registrar **explícitamente** `superadmin_bp` y crear **stubs** mínimos para evitar roturas hasta implementar CRUD completo.

4. Import obsoleto `from app.core import *`  
   - Causa: Restos de versiones anteriores.  
   - Solución: Eliminarlo en rutas; limitar uso de `db` a modelos y evitar imports circulares.

5. Navbar visible en login  
   - Solución: `base_auth.html` y `login.html` extendiendo esa base.

## Estado actual
- **/login**: operativo (usa `base_auth.html`).
- **/superadmin/dashboard**: operativo con tarjetas azules.
- **/superadmin/bufetes** y **/superadmin/bufetes/nuevo**: stubs que no rompen.
- **/superadmin/usuarios**: stub operativo.
- **/dashboard** (bufete general): carga como antes (colores del dashboard general intactos).

## Próximos pasos sugeridos
1. Implementar CRUD real de **Bufetes** (WTForms + validaciones + commit DB).  
2. Implementar CRUD real de **Usuarios** (generación de username B{bufete}_{rol}{n}_{inicial+apellido}, hash de password, estados).  
3. Validaciones NIT/DPI (lib `NIT-dpi-validator`) y soporte regional.  
4. Decoradores/permisos finos y auditoría mínima (tablas + middleware).  
5. Pruebas rápidas de rutas y de login (smoke tests).

## Git propuesto
Rama actual: `feature/docs_y_dashboards`

Comandos sugeridos:
```bash
git add app/__init__.py app/models/usuarios.py app/auth app/superadmin app/templates/base.html app/templates/base_auth.html app/templates/partials app/utils/roles_required.py app/utils/permisos.py docs/README_SABADO_090825.md
git commit -m "Login estable; dashboard SuperAdmin azul; stubs Bufetes/Usuarios; base_auth; helpers de roles y permisos (090825)"
git push -u origin feature/docs_y_dashboards

# Tag del hito
git tag -a sat-fix-090825 -m "Hito: login y superadmin dashboard estable (09/08/25)"
git push origin sat-fix-090825
```

## Nota final
Para la próxima sesión, pedir **un único ZIP** con todos los archivos ajustados y pruebas básicas para evitar loops. Ver “PROMPT DE REINICIO” adjunto.
