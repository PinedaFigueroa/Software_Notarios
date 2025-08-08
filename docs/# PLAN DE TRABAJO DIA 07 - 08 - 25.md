# PLAN DE TRABAJO DIA 07 - 08 - 25 
🚀 Confirmado, Giancarlo.

Reconozco este nuevo prompt como parte **oficial** del:

```
🧱 Proyecto: Software Notarios
🧩 Bloque 3 – Planes, Bufetes y Roles/Usuarios
📍 Subfase actual: A. Dashboards diferenciados
🗓️ Fecha de continuación: 07 / 08 / 2025
📁 Entorno: BDD limpia + seed inicial + Bootstrap local funcionando
```

---

## ✅ Confirmación y Siguiente Paso

Estás en lo correcto: **el punto de partida debe ser la implementación del login**, ya que:

* Permite identificar el `rol` del usuario en sesión.
* Desde ahí redirigimos al **dashboard correspondiente**:

  * `SuperAdmin` → acceso global (gestión de bufetes, usuarios, planes, estadísticas)
  * `Usuarios de bufete` → acceso local al dashboard de su bufete (como ya está funcionando)

---

## 🔧 SIGUIENTE ACTIVIDAD: LOGIN Y DASHBOARD DIFERENCIADO

### 📌 Paso 1: Implementar login con Flask-Login

**Objetivo**: Activar un formulario de login funcional, registrar sesión, y según el rol, redirigir a su dashboard.

### 📂 Archivos clave involucrados:

* `app/auth/routes.py` (blueprint de autenticación)
* `app/templates/auth/login.html` (formulario visual)
* `app/models/usuarios.py` (método `is_authenticated`, `get_id`, etc.)
* `app/__init__.py` (configuración de `LoginManager`)
* `app/utils/roles_required.py` (decoradores para permisos)

---

### ✅ Actividades puntuales a realizar:

1. [ ] Crear blueprint `auth_bp` en `app/auth/`
2. [ ] Crear `login.html` con formulario de email + password
3. [ ] Implementar `LoginManager` en `app/__init__.py`
4. [ ] Método `load_user()` que recupere usuarios desde la BDD
5. [ ] Configurar redirección:

   * `SuperAdmin` → `/admin/dashboard`
   * `Otros` → `/dashboard`
6. [ ] Decoradores `@login_required` y `@rol_required(['SuperAdmin'])`
7. [ ] Control de logout
8. [ ] Mostrar en navbar si hay sesión activa (y quién es)

---

¿Procedemos con la estructura base del login y el blueprint `auth_bp`?
Puedo generar de una vez:

* Estructura del folder `auth/` con `routes.py`, `forms.py`
* Login HTML
* Configuración inicial de Flask-Login
* Decoradores de control de acceso

Dame el visto bueno y lo armo para que lo tengas listo para usar y testear.
