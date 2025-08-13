# README IMPLEMENTACION PLANES 12 - 08 - 25
¡Listo, partner! Incorporé tus puntos y dejé todo empaquetado para que avances sin tropiezos.

# Qué hice

* Integré tus decisiones y criterios (incluido lo de 1 administrador mínimo por bufete, ocultar SUPERADMIN en UI, y validación DPI/NIT centralizada) en un **documento técnico** para `\docs`.
* Te dejé un **ZIP con el CRUD de Planes** + parches:

  * CRUD completo (rutas, formularios, plantillas, paginación, tooltips).
  * Bufetes: formulario ampliado con **todos** los campos del modelo y `Select` de **Plan**.
  * Usuarios: UI sin `SUPERADMIN` y validación **servidor**; reglas para **no dejar un bufete sin administrador**.
  * Validadores GT centralizados (DPI/NIT) listos para reusar en cualquier form.
  * Partial opcional para el navbar con “Planes”.

# Descargas

* Documento (para guardar en `\docs`):

  * [arquitectura\_planes\_bufetes\_usuarios.md](sandbox:/mnt/data/docs/arquitectura_planes_bufetes_usuarios.md)
* Paquete de código:

  * [superadmin\_planes\_crud\_130825.zip](sandbox:/mnt/data/superadmin_planes_crud_130825.zip)

# Cómo aplicar (paso a paso)

1. **Descomprime el ZIP** en la raíz del proyecto (sobrescribe archivos si te lo pide).
2. Asegura en `app/superadmin/__init__.py`:

   ```python
   from . import routes_planes  # noqa
   ```
3. **Instala validadores Guatemala**:

   ```
   pip install nit-dpi-validator
   ```
4. (Si corresponde) Migraciones:

   ```
   flask db migrate -m "CRUD planes + validadores GT + UI cambios"
   flask db upgrade
   ```
5. **Opcional**: usa el partial `_navbar_superadmin.html` del ZIP (ya incluye “Planes”).

# Resumen de las reglas implementadas

* **Planes**: CRUD de SuperAdmin. Si un plan tiene bufetes asociados, no se elimina: se **desactiva**.
* **Bufetes**: formulario con todos los campos, **validación NIT** (tanto `nit` como `facturacion_nit`), y **select de Plan** (solo planes activos).
* **Usuarios**:

  * **UI** sin rol `SUPERADMIN`.
  * **Servidor** rechaza crear/asignar `SUPERADMIN` vía interfaz.
  * **Regla 1 Admin mínimo**: no permite eliminar ni “degradar” al último ADMINISTRADOR del bufete.
* **Validadores GT**:

  * `app/validators/gt.py` expone `validate_nit` y `validate_dpi` (llaman a `nit-dpi-validator` si está instalada). Los forms llaman a estas funciones para centralizar la lógica.
  * DPI queda listo para usarse cuando metas el campo en `Usuario` (post RRHH), que es coherente con tu visión.
* **Seguridad/ISO/OWASP**: el doc mapea a ISO/IEC 27001 (A.9, A.12, A.13, A.14) y OWASP ASVS (validación, sesiones, etc.).

# Siguientes pasos sugeridos

1. **Git snapshot** del estado actual (lo de hoy).
2. Aplica el **ZIP** y prueba:

   * `/superadmin/planes` (crear/editar/desactivar).
   * Crear/editar **bufete** asignando plan.
   * Crear/editar/eliminar (lógico) **usuario** verificando la regla de **admin mínimo**.
3. Si todo entra limpio, haz **commit** del bloque “Planes → Bufetes → Usuarios”.

¿Te va bien así? Si te tira algún traceback, pégamelo tal cual y te doy el parche exacto.
