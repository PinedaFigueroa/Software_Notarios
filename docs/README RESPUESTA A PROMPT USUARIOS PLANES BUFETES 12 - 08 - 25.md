# README RESPUESTA A PROMPT USUARIOS PLANES BUFETES 12 - 08 - 25

¡bravísimo! ya creaste un bufete y un usuario 🎯. Tomo tu “refresh” y te dejo un plan técnico-estricto para dejar esto nítido, con criterios de diseño, seguridad y operación alineados a buenas prácticas (ISO/IEC 27001, OWASP ASVS) antes del commit grande.

# 1) Principios base (estables)

* **Nomenclatura**: blueprint `superadmin_bp = Blueprint('superadmin', ...)` y siempre `url_for('superadmin.*')`.
* **Soft delete**: `BufeteJuridico.activo`, `Usuario.borrado_logico` (hoy correcto). Agrega filtros por defecto en queries de listas.
* **Migrations**: una por bloque funcional (planes → bufetes→ usuarios), con `downgrade` claro.
* **Config separada**: `Config/Dev/Prod` (SECRET\_KEY, DB, DEBUG, LOG\_LEVEL). Secrets solo por env vars.

# 2) CRUD de Planes (bloque inmediato)

Objetivo: que SuperAdmin gestione catálogo de planes y que Bufete se amarre a `plan_id`.

**Modelo** (ya tienes `Plan` 👌). Añade índices:

* `nombre` unique (ya), **índice** en `(activo, nombre)` para listados.
* Opcional: `precio_mensual` index si filtras por rango.

**Forms**
`PlanForm`: `nombre`, `descripcion`, `max_*`, `max_documentos`, `storage_mb`, `precio_mensual`, `es_personalizado`, `activo`.
Validaciones:

* `nombre` requerido, único, ≤100.
* `precio_mensual` ≥ 0.
* `max_*`, `max_documentos`, `storage_mb` enteros ≥ 0.

**Rutas** (`/superadmin/planes`):

* Listar (paginado), Crear, Editar, Eliminar lógico (`activo=False`).
* **Regla de integridad**: si un plan tiene bufetes asociados, **no permitir “eliminar”**; solo *desactivar* (para no ofrecerlo a nuevos bufetes).

**Templates**

* Tabla con badges: `activo`, `es_personalizado`.
* Tooltips (Bootstrap) con `data-bs-toggle="tooltip"` y `title` en labels y acciones.

**Vínculo con Bufetes**

* En `BufeteForm`, `SelectField plan_id` → opciones: `Plan.query.filter_by(activo=True)`.
* Al editar plan de un bufete, mostrar **aviso** si los límites actuales del bufete (usuarios/doc) exceden el nuevo plan (solo warning; no bloquear por ahora).

# 3) Bufetes (campos completos y validación)

Amplía el form para cubrir los campos del modelo:

* Datos: `nombre_bufete`*, `direccion`, `telefono`, `email`, `nit`, `pais`, `forma_contacto`, `plan_id`*.
* Facturación: `facturacion_nombre`, `facturacion_nit`, `facturacion_direccion`.
* Métodos de pago: `formas_pago` (multi-opción), `metodo_pago_preferido`.
* Flags: `maneja_inventario_timbres_papel`, `incluye_libreria_plantillas_inicial`, `habilita_auditoria_borrado_logico`, `habilita_dashboard_avanzado`, `habilita_ayuda_contextual`, `habilita_papeleria_digital`.
* Validaciones:

  * `nombre_bufete` requerido + único.
  * `email` formato email (WTForms `Email`).
  * `telefono` con regex suave.
  * `nit` opcional (puede venir “CF”).
  * `pais` opcional.
  * `plan_id` requerido (siempre tener plan).
* **Index sugeridos**: `idx_bufete_activo` en `activo`, `idx_bufete_plan` en `plan_id`.

# 4) Usuarios (roles y seguridad)

* **Roles en UI**: oculta `SUPERADMIN` del `SelectField`.

  * UI: choices = {ADMINISTRADOR, NOTARIO, PROCURADOR, ASISTENTE}.
  * **Servidor**: enforce → si llega `SUPERADMIN`, rechazar salvo que `current_user.rol == SUPERADMIN` y `ALLOW_SUPERADMIN_CREATION=True` en config (por defecto False).
* Campos: `username`*, `correo`, `password`, `rol`, `bufete_id`*, (opcional futuro `dpi`).
* Password: `werkzeug.security` (PBKDF2) ya ok. Reglas: min length 8, complejidad moderada.
* **Index/constraints**: `username` unique; `idx_user_bufete` en `bufete_id`; `idx_user_borrado` en `borrado_logico`.
* **Single-session** (visión): tabla `user_sessions` (user\_id, session\_id, issued\_at, revoked\_at). En login, invalidar sesión previa del usuario (o permitir 1 por user/rol).

# 5) Auditoría y trazabilidad (base ya)

Añade un **módulo de auditoría** mínimo desde ya:

* Modelo `AuditEvent(id, user_id, bufete_id, action, resource_type, resource_id, metadata JSON, ip, user_agent, ts)` + índice por `(bufete_id, ts)` y por `user_id`.
* Helper `audit(action, resource, id, **meta)` y decoradores para rutas críticas.
* Log a archivo JSON (`logs/app.jsonl`) con rotación.
* Eventos clave: login/logout (resultado), crear/editar/eliminar (bufete, usuario, plan), intento de acceso fuera de oficina (ver #6).

> ISO 27001 A.12 (operaciones de seguridad) y A.16 (gestión de incidentes) — eventos trazables y alertables.

# 6) Restricción por oficina (IP allowlist)

* Tabla `AllowedIPRange(id, bufete_id, cidr, activo)`; si un bufete no define rangos, política “solo oficina” global de SuperAdmin o **denegar** por defecto (decisión de negocio).
* Middleware (`@app.before_request`) que, si `current_user` autenticado y no SUPERADMIN, verifique `request.remote_addr` ∈ allowlist del bufete.
* En fallo: `403`, disparar `audit("login_denegado_ip", ...)` y **notificación** al dashboard del superadmin (banner o card “Seguridad”).
* **Excepciones**: registro temporal por horas con autorización explícita (otra tabla con expiración).

> ISO 27001 A.9 (control de acceso) y A.13 (seguridad de comunicaciones).

# 7) UX/UI profesional

* **Paleta** (abogados): base azul/gris, acentos discretos; rojo/amarillo exclusivos para error/alerta.

  * Define **CSS variables** (p. ej. en `static/css/variables.css`):
    `--brand-600: #0d6efd; --neutral-100: #f6f8fb; --text-900: #0b132b; --success-600; --warning-600; --danger-600;`
  * Usa variables en botones/cards, evita colores “duros” inline.
* **Nav (top→bottom, left→right)**: orden consistente: Dashboard → Planes → Bufetes → Usuarios → Documentos → Librería → Reportes → Ayuda.
* **Paginación** en listados (25 por página).
* **Tooltips**: agrega `data-bs-toggle="tooltip"` y en el layout:

  ```html
  <script>var t=document.querySelectorAll('[data-bs-toggle="tooltip"]');[...t].map(el=>new bootstrap.Tooltip(el));</script>
  ```
* **Accesibilidad**: contraste AA mínimo; `aria-label` en botones (Editar/Eliminar).
* **Mensajería**: usa `flash` con categorías (`success`, `info`, `warning`, `danger`) y estilos coherentes.

# 8) Reportes internos (visión e infraestructura)

* Por bufete: #documentos, rechazos, costos (si módulo timbres), carga por procurador, errores, etc.
* Prepara **tabla materializada** / vistas o **tareas en background** a futuro (por ahora, queries simples + índices).
* Cards en dashboard del superadmin con **señales**: “Intentos de acceso fuera de oficina”, “Usuarios inactivos”, “Planes por expirar”.

# 9) Seguridad adicional (OWASP ASVS / ISO)

* Cookies de sesión: `SESSION_COOKIE_SECURE=True` (en prod), `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`.
* **CSRF** activo (ya).
* **Rate limiting** en login (Flask-Limiter): p.ej. `5/min` por IP + `10/min` por username.
* **Lockout** progresivo tras intentos fallidos.
* **Headers**: `X-Frame-Options: DENY`, `Content-Security-Policy` mínimo (self para scripts/estilos locales).
* **Backups** y restauración probada; sellar versiones (git tags).
* **Rastros de cambios de configuración** (planes, flags de bufete).
* **Sin SUPERADMIN en UI** (ya definido arriba).

# 10) Semillas (seed) y datos

* Mantén el **seed de planes** (Demo/Profesional/Ilimitado).
* Seed de **bufete principal** ligado a “Profesional”.
* Seed de **superadmin** 1 único + notario principal.
* Añade **checks** de idempotencia (ya los tienes bien).

---

## Checklist para el commit “todo lo de hoy”

1. Endpoints normalizados a `superadmin.*` ✅
2. Templates corregidos (comentarios Jinja, `hidden_tag()`, sin `hasattr`) ✅
3. Login redirecciona a `superadmin.dashboard_global` ✅
4. CRUD Bufetes/Usuarios funcionando (mínimo) ✅
5. Crear **CRUD Planes** (nuevo bloque) → incluir forms, rutas, plantillas y paginación.
6. Bufete: ampliar form con todos los campos del modelo + `plan_id`.
7. Usuarios: ocultar `SUPERADMIN` en UI y **validar en servidor**.
8. Añadir **módulo de auditoría** (modelo + helper + hooks básicos).
9. Añadir **allowlist de IP** por bufete (infra lista aunque lo actives más adelante).
10. Variables CSS de paleta y tooltips Bootstrap.

Si te parece, en el siguiente bloque te genero el **CRUD de Planes** (rutas, forms y templates ya con tooltips + paginación) y un **patch** para expandir Bufetes con todos los campos y select de Plan, y restringir roles en Usuarios. También puedo preparar un **commit message** sugerido y la lista de migraciones (`flask db migrate -m "..."` → `flask db upgrade`).
