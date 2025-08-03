## 1️⃣ Definir cómo se autentican los usuarios

**Opción A: Usuario y contraseña**

* Campo `usuario` (username único por bufete o global para superadmin).
* Campo `password_hash` para seguridad.
* No depende de correo electrónico.
* Superadmin puede iniciar sesión solo con su usuario y contraseña.

**Opción B: Usuario + correo (opcional)**

* Para bufetes grandes, podríamos usar correos.
* Pero sigue siendo opcional para no bloquear el flujo de superadmin.

💡 **Recomendación**:
Ir con **Opción A**. En el modelo `Usuario` usaremos `username` (ej. `superadmin` o `B1_N1_giancarlo`) y `password_hash`.
El login pedirá solo **usuario y contraseña**.

---

## 2️⃣ Ajustar modelo `Usuario`

Si tu `Usuario` actual no tiene `username` ni `password_hash`, agregamos:

```python
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(RolUsuarioEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

---

## 3️⃣ Login para Superadmin

* En `auth/routes.py`, reemplazamos `email` por `username`.
* El formulario solo pedirá:

  1. **Usuario**
  2. **Contraseña**

```python
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.models.usuarios import Usuario

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Bienvenido, {user.nombre_completo}", "success")
            return redirect(url_for("dashboard.mostrar_dashboard"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("auth/login.html")
```

---

## 4️⃣ Ajustar el Seed

Cuando creamos el **superadmin**, debemos darle un `username` y un `password_hash`:

```python
superadmin = Usuario(
    nombre_completo="Super Admin",
    username="superadmin",
    rol=RolUsuarioEnum.SUPERADMIN,
)
superadmin.set_password("1234")  # 🔹 Cambiar en producción
db.session.add(superadmin)
db.session.commit()
```
