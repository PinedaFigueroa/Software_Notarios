# Arquitectura y Estándares — Planes, Bufetes, Usuarios
**Fecha:** 13/08/2025  
**Responsables:** Giancarlo F. + Tars-90

> Objetivo: Dejar lineamientos y piezas base para cerrar el bloque **Planes → Bufetes → Usuarios** con criterios de seguridad (ISO/IEC 27001), desarrollo seguro (OWASP ASVS) y UX profesional.

---

## 1. Principios rectores
- **Blueprints y endpoints canónicos**: `superadmin_bp = Blueprint('superadmin', ...)` y uso de `url_for('superadmin.*')` en toda la app.
- **Borrado lógico**: `BufeteJuridico.activo`, `Usuario.borrado_logico`. Todas las listas filtran por defecto registros activos/no borrados.
- **Migraciones**: una por bloque funcional (planes → bufetes → usuarios). Mantener downgrade.
- **Config**: `Config/Dev/Prod` con secretos por variables de entorno.

## 2. Reglas de negocio
- **Al menos un ADMINISTRADOR por bufete**  
  - Cualquier bufete debe contar siempre con **≥ 1** usuario con rol **ADMINISTRADOR** (normalmente un Notario).  
  - Está prohibido dejar un bufete sin administrador por eliminación/borrado lógico o cambio de rol.
- **SUPERADMIN no se crea desde UI**  
  - El rol `SUPERADMIN` **no** aparece en la UI de creación/edición de usuarios.  
  - Se puede crear/gestionar sólo por seed/CLI/ops (config `ALLOW_SUPERADMIN_CREATION=False`).
- **Planes**  
  - `Plan` se gestiona por SuperAdmin (CRUD).  
  - `BufeteJuridico` debe estar asociado a un `Plan` activo (select en el form).  
  - Si un plan tiene bufetes asociados, no se elimina; sólo **desactivar** (`activo=False`).

## 3. Validaciones Guatemala (DPI / NIT)
- Dependencia: [`nit-dpi-validator`](https://pypi.org/project/nit-dpi-validator/).  
- **Globalización de validadores**: módulo `app/validators/gt.py` con helpers:
  - `validate_nit(value) -> (ok, error_msg)`
  - `validate_dpi(value) -> (ok, error_msg)`
- Integración inicial:
  - `BufeteJuridico.nit` y `facturacion_nit` → validación **NIT** (opcional si el campo no está vacío).
  - En Usuarios, **DPI** se incorporará cuando el campo esté en el modelo (post RRHH). Por ahora, sólo infraestructura.
- **NIT para todos** (visión): se fomenta capturar NIT de usuarios internos (procuradores/asistentes) para facturación al bufete; campo a introducir en un próximo migration.

## 4. Seguridad y cumplimiento (ISO/IEC 27001, OWASP ASVS)
- **A.9 / ASVS-2** Control de acceso: rol `SUPERADMIN` restringido; 1 admin mínimo por bufete; verificación de IP/allowlist por bufete (infra preparada).
- **A.12 / ASVS-9** Operación segura y auditoría: registrar login/logout, CRUD de planes/bufetes/usuarios, intentos fuera de oficina.
- **A.13** Seguridad de comunicaciones: cookies de sesión `HttpOnly`, `Secure` (prod), `SameSite=Lax`.
- **A.14** Gestión de cambios: migraciones versionadas por bloque.
- **ASVS-3/4** Validación entrada: DPI/NIT con librería certificable; server-side y mensajes claros de error.
- **ASVS-5** Control de sesiones: “un usuario, una sesión” (infra a definir con `user_sessions`).

## 5. UX y consistencia visual
- Paleta sobria (azules/grises); rojo/amarillo reservados a alertas. Variables CSS propias.
- Navbar (izq→der): **Dashboard | Planes | Bufetes | Usuarios | Documentos | Librería | Reportes | Ayuda**.
- Tooltips con Bootstrap en iconos y labels para discovery inmediato.
- Paginación (25 por página) y mensajes `flash` consistentes (`success/info/warning/danger`).

## 6. Roadmap del bloque
1. **CRUD Planes** (este paquete): catálogo, activar/desactivar, paginación.  
2. **Bufetes** ampliado: todos los campos + select de plan con validación NIT en `nit` y `facturacion_nit`.  
3. **Usuarios**: ocultar `SUPERADMIN` en UI, enforcement servidor; regla **≥ 1 admin** por bufete.  
4. **Auditoría** mínima (“quién, qué, cuándo, desde dónde”).  
5. **Allowlist IP** por bufete (middleware) y alertas en dashboard del SuperAdmin.

---

## 7. Instrucciones de despliegue del bloque
1. **Instalar dependencia (validadores Guatemala):**
   ```bash
   pip install nit-dpi-validator
   ```
2. **Aplicar el ZIP de CRUD Planes + Parches (ver archivo adjunto).**
3. **Migraciones (si aplica)**:
   ```bash
   flask db migrate -m "CRUD planes + validadores GT + UI cambios"
   flask db upgrade
   ```
4. **Seed de planes**: ya presente en `app/cli.py` (`seed-cli init`).

---

## 8. Decisiones abiertas
- Incorporar **DPI** y **NIT** a `Usuario` (migración posterior, enlazado a RRHH).  
- “Una sesión por usuario”: requiere modelo de sesión y middleware.  
- Alertas de seguridad (intentos fuera de oficina): cards en dashboard del SuperAdmin.

---

### Anexo: Endpoints
- `superadmin.planes_listar` `/superadmin/planes`
- `superadmin.plan_nuevo` `/superadmin/planes/nuevo`
- `superadmin.plan_editar` `/superadmin/planes/<int:plan_id>/editar`
- `superadmin.plan_eliminar` `/superadmin/planes/<int:plan_id>/eliminar` (desactivar)
- `superadmin.listar_bufetes` `/superadmin/bufetes`
- `superadmin.crear_bufete` `/superadmin/bufetes/nuevo`
- `superadmin.editar_bufete` `/superadmin/bufetes/<int:bufete_id>/editar`
- `superadmin.eliminar_bufete` `/superadmin/bufetes/<int:bufete_id>/eliminar`
- `superadmin.listar_usuarios` `/superadmin/usuarios`
- `superadmin.crear_usuario` `/superadmin/usuarios/nuevo`
- `superadmin.editar_usuario` `/superadmin/usuarios/<int:usuario_id>/editar`
- `superadmin.eliminar_usuario` `/superadmin/usuarios/<int:usuario_id>/eliminar`
