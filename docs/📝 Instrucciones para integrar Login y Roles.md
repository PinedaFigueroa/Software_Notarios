# 📝 Instrucciones para integrar Login y Roles (feature/login\_roles)

## 1. Archivos incluidos en `feature_login_roles.zip`

```
app/
 └─ auth/
     ├─ __init__.py
     └─ routes.py
app/templates/
 └─ auth/
     └─ login.html
app_init_update.txt  # guía de integración
```

---

## 2. Registrar el Blueprint `auth_bp` en `app/__init__.py`

Editar tu `create_app()` e **importar y registrar el blueprint**:

```python
from app.auth import auth_bp  # NUEVO

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Registrar blueprints
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")  # NUEVO

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'  # Redirige si no está logueado

    # Registrar comandos personalizados
    from app.cli import cli
    app.cli.add_command(cli)

    return app
```

---

## 3. Ajustar `Usuario` para Flask-Login

En tu modelo `Usuario` (`models/usuarios.py`):

```python
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    # ...
    # Asegúrate de tener:
    # - id como primary key
    # - atributo "activo" o "estado" para validar login

    def get_id(self):
        return str(self.id)
```

En `app/__init__.py`:

```python
@login_manager.user_loader
def load_user(user_id):
    from app.models.usuarios import Usuario
    return Usuario.query.get(int(user_id))
```

---

## 4. Rutas principales en `auth/routes.py`

* **`/auth/login`**: Muestra el formulario de login.
* **`/auth/logout`**: Cierra sesión y redirige a login.
* Protege el dashboard con `@login_required`.

---

## 5. Forzar login antes de dashboard

En `app/dashboard/routes.py`:

```python
from flask_login import login_required

@dashboard_bp.route("/dashboard")
@login_required
def mostrar_dashboard():
    ...
```

---

## 6. Probar la integración

1. Activar tu entorno virtual
2. Ejecutar la app:

```bash
flask run
```

3. Abrir en el navegador:

   * **[http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login)**
   * Al iniciar sesión, te redirige al **Dashboard**
   * Logout disponible en `/auth/logout`

---

## 7. Próximos pasos

* Crear un **usuario Superadmin** válido en la BDD para poder loguearse.
* Luego probar crear bufetes y roles.
* Implementar manejo de **alertas y métricas** con colores definidos.

