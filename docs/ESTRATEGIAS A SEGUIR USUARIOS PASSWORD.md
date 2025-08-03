# ESTRATEGIAS A SEGUIR USUARIOS PASSWORD

---

### 🔹 Contexto real del proyecto

1. **Aplicación interna / controlada**

   * Los bufetes **no se registran solos** ni los usuarios tampoco.
   * **Superadmin** crea bufetes y usuarios según el plan adquirido.
   * Usuarios acceden con un **username** predefinido (`B1_N1_JuanPerez` o `superadmin`).
   * No hay registro público → No se valida correo al inicio.

2. **Aplicación abierta / pública** (fase futura)

   * Permitir que cualquier bufete se registre, pague, y cree sus usuarios.
   * Ahí sí **requiere email** (para verificación, recuperación de contraseña, notificaciones).
   * Debemos validar correos y eventualmente forzar verificación (token/email).

---

### 🔹 Pros y contras

**Si usamos solo `username` (controlada):**

✅ Más rápido implementar
✅ No hay riesgo de emails falsos
✅ Control total por superadmin
✅ Ideal para fase beta o cliente cerrado

❌ No permite registro autónomo
❌ Recuperación de contraseña solo manual (via superadmin)

---

**Si usamos `email` (pública):**

✅ Estandarizado para login web
✅ Permite autogestión de contraseñas
✅ Más fácil de escalar a SaaS

❌ Necesitamos validar emails
❌ Riesgo de spam / registros basura
❌ Mayor complejidad en esta etapa

---

### 🔹 Recomendación

Por lo que me describes, **estamos en fase controlada**, donde:

* Solo **Superadmin** crea bufetes y usuarios.
* **Usuarios usan un username estándar** (ejemplo: `B1_N1_JuanPerez`).
* **Password** inicial definido por superadmin, luego puede cambiarse.
* **Email opcional**, para notificaciones futuras, pero **no obligatorio** para login.

He analizado a fondo tu planteamiento y te propongo una **arquitectura profesional y escalable**, que cubre tanto la versión controlada actual como la futura versión pública, siguiendo estándares de **seguridad, auditoría y mantenibilidad**.

---

## 1️⃣ Identidad del Usuario

### Problema

* No podemos garantizar **nombre único global**: existen homónimos (`Juan Perez`, `Juan P. Gonzalez`).
* No queremos depender solo de **email** porque:

  1. En la versión controlada, un bufete puede usar un único correo para todos.
  2. Email único solo será relevante en versión pública.

### **Propuesta**

* **ID interno (`id`)**: Clave primaria para todas las referencias.
* **Username único global (`username`)**:

  * Formato recomendado: `BUFETEID_ROL_INDEX_nombre`
    Ej: `B1_N1_giancarlo`
  * Evita homónimos sin depender de email.
  * Sirve para login en versión controlada.
* **Nombre completo (`nombre_completo`)**:

  * Obligatorio, para auditoría y reportes.
  * Se guarda tal cual lo escribe el superadmin al crear el usuario.

---

## 2️⃣ Modelo `Usuario` Profesional

```python
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class RolUsuarioEnum(enum.Enum):
    SUPERADMIN = "superadmin"
    NOTARIO = "notario"
    PROCURADOR = "procurador"
    ASISTENTE = "asistente"
    ADMIN_LOCAL = "admin_local"

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    bufete_id = db.Column(db.Integer, db.ForeignKey("bufetes_juridicos.id"), nullable=True)

    nombre_completo = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Login principal
    email = db.Column(db.String(150), unique=False, nullable=True)    # Único en versión pública
    password_hash = db.Column(db.String(255), nullable=False)

    rol = db.Column(db.Enum(RolUsuarioEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    ultimo_login = db.Column(db.DateTime, nullable=True)

    # Seguridad: para limitar sesiones simultáneas
    session_token = db.Column(db.String(255), nullable=True, unique=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
```

**Ventajas:**

* `username` único global garantiza login limpio.
* `bufete_id` permite multi-tenant sin colisiones de nombres.
* `session_token` permite controlar que un usuario no abra 10 sesiones simultáneas.
* `email` es opcional ahora, obligatorio en versión pública.
* Listo para **auditoría**, **seguridad** y **escalabilidad internacional**.

---

## 3️⃣ Estrategia de Login

### Versión controlada (actual)

* Login solo con `username` + `password`.
* Control de sesiones:

  * Generar `session_token` al hacer login.
  * Invalidar token anterior si se detecta login en otra máquina.

### Versión pública (futura)

* Login con `username` **o** `email`.
* Email único y validado antes de permitir registro.
* Opcional: verificación en dos pasos para superadmin y planes premium.

---

## 4️⃣ Estrategia de Auditoría

1. **Auditoría básica** integrada:

   * `fecha_creacion`, `fecha_actualizacion`, `ultimo_login`
2. **Trazabilidad de sesiones**:

   * Cada login genera `session_token`.
   * Se guarda en la base y en la cookie de sesión.
3. **Logs**:

   * Registrar inicios y cierres de sesión.
   * Detectar intentos fallidos y bloquear si es necesario.

---

## 5️⃣ Estrategia de Creación de Usuarios

1. **Superadmin** crea bufetes y usuarios.
2. **Reglas**:

   * `nombre_completo` obligatorio.
   * `username` generado siguiendo patrón `B{bufete_id}_{rol}_{index}_{nombre}`.
   * Confirmación para evitar duplicados de nombre (homónimos).
3. **Control de auditoría**:

   * Guardar quién creó cada usuario y en qué fecha.

---

## 6️⃣ Escalabilidad y Estándares

* **SQLAlchemy + Flask-Login** → estándar de la industria.
* **Passwords con hash seguro** (Werkzeug).
* **Multi-tenant** desde el diseño (`bufete_id`).
* **Preparado para internacionalización** y despliegue en nube.
* **Control de sesiones simultáneas** listo para activar en producción.

---

💡 **Conclusión profesional**:

* Mantener `username` único global.
* `nombre_completo` para auditoría, `email` opcional.
* Guardar `session_token` para limitar sesiones.
* Preparar login con `username` y opcionalmente `email` en el futuro.

---

Si quieres, puedo prepararte **el modelo `Usuario` + seed + login** ya con esta arquitectura y control de sesión listo para versión controlada y escalable.

¿Quieres que lo haga en un único paquete funcional para integrarlo ahora mismo?
