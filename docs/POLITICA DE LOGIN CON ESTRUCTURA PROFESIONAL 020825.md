# POLITICA DE LOGIN CON ESTRUCTURA PROFESIONAL
---

## 1️⃣ Flujo de Login Profesional

1. **Formulario de Login**:

   * `username` (asignado por superadmin o bufete)
   * `password` inicial
2. **Validaciones**:

   * Username existe y está activo
   * Password correcto (`check_password`)
   * Control de sesiones simultáneas con `session_token`
3. **Primera vez**:

   * Si es primer login o password expirado → obligar cambio de contraseña.
4. **Redirección**:

   * Muestra dashboard correspondiente al `rol` del usuario:

     * **Navbar**: Nombre completo + Bufete
     * **Contenido**: Documentos, tareas, reportes según permisos

---

## 2️⃣ Política de Contraseñas Segura

* **Longitud mínima**: 8-12 caracteres
* **Complejidad**: mayúsculas, minúsculas, números y símbolo
* **Expiración**: cada 3 meses
* **Primera vez**: debe cambiar la contraseña

### 🔹 Librerías recomendadas en Python

Podemos usar `password_strength` o `validators` para validar complejidad:

```bash
pip install password-strength
```

```python
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,    # Mínimo 8 caracteres
    uppercase=1, # Al menos 1 mayúscula
    numbers=1,   # Al menos 1 número
    special=1,   # Al menos 1 caracter especial
    nonletters=0 # No requiere simbolos extra
)

if policy.test(password):
    # Devuelve lista de errores si no cumple
    return "La contraseña no cumple con los requisitos"
```

---

## 3️⃣ Modelo `Usuario` con Control de Password y Expiración

```python
from datetime import datetime, timedelta

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    bufete_id = db.Column(db.Integer, db.ForeignKey("bufetes_juridicos.id"), nullable=True)
    
    nombre_completo = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    rol = db.Column(db.Enum(RolUsuarioEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    ultimo_login = db.Column(db.DateTime, nullable=True)
    password_expira = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=90))
    
    session_token = db.Column(db.String(255), nullable=True, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password_expira = datetime.utcnow() + timedelta(days=90)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def password_expired(self):
        return datetime.utcnow() > self.password_expira
```

---

## 4️⃣ Dashboard por Rol

Al iniciar sesión:

* **Navbar**:

  * `{{ current_user.nombre_completo }}`
  * `{{ current_user.bufete.nombre }}` (relación con bufete)
* **Contenido dinámico**:

  * Si es **notario** → documentos propios
  * Si es **procurador** → tareas asignadas
  * Si es **asistente** → avisos y soporte
  * Si es **superadmin** → gestión de bufetes y usuarios

---

## 5️⃣ Auditoría y Seguridad Extra

1. **Control de sesiones simultáneas**:

   * Guardar `session_token` único por login
   * Si inicia sesión en otro dispositivo, invalidar la anterior
2. **Logs de acceso**:

   * Guardar `ultimo_login`
   * Guardar IP de acceso para auditoría (opcional)
3. **Bloqueo por intentos fallidos**:

   * 3-5 intentos → bloqueo temporal de 15 minutos

---

💡 **Beneficio**:
Con esta arquitectura tendrás un sistema **seguro, auditado y profesional**, que está listo para:

1. **Versión controlada** → login por username.
2. **Versión pública futura** → login por username/email, password policies y 2FA opcional.

---

** EN RESUMEN **

1. `Usuario` con control de expiración de password
2. Seed inicial para superadmin
3. Rutas de login con validación de complejidad
4. Middleware para forzar cambio de password si expiró
