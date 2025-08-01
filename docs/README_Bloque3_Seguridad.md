# Software Notarios - Bloque 3: Seguridad y Roles
## Fecha: DD/MM/AAAA

### ✅ Avances
- Integración de Flask-Login
- Sistema de login y logout funcional
- Decoradores de permisos (`@requires_role`) implementados
- Redirección a dashboard según rol

### 🐞 Errores y Soluciones
- (Ejemplo) Sesión no persistía → Solución: configurar `SECRET_KEY` en `app.config`
- Ajuste en `permisos.py` para múltiples roles

### 📄 Código y Archivos Relevantes
- `app/utils/permisos.py`
- `app/dashboard/routes.py` (rutas protegidas)
- Configuración de Flask-Login en `app/__init__.py`

### 📌 Pendientes
- Protección completa de todos los blueprints
- Crear formulario de login visual con Bootstrap
