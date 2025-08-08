# Informe técnico: Ajustes de Login y Blueprints (07/08/2025)

## 🔧 Archivos corregidos
- `auth/forms.py`: se corrigió el import erróneo (`flask_wt`) y se validó el formulario básico.
- `auth/routes.py`: se corrigió el uso de `usuario.password` a `usuario.password_hash`.
- `auth/__init__.py`: se agregó el docstring que estaba faltando.

## 🐞 Error detectado
Durante el login se intentaba acceder a un atributo inexistente `usuario.password`, cuando en el modelo se había definido como `password_hash`. Esto causaba un `AttributeError` y una pantalla 500 sin mensaje claro al usuario.

## ✅ Solución aplicada
- Se usó `check_password_hash(usuario.password_hash, form.password.data)`.
- Se agregó validación correcta al formulario de login.
- Se añadió `flash()` para retroalimentación inmediata al usuario.

## 🔒 Recomendaciones futuras
- En producción se validará también correo electrónico.
- El flujo actual está pensado para usuarios creados centralizadamente por el `superadmin`.
- Se planea forzar cambio de contraseña al primer login (aún pendiente de implementación).

---
🕒 Fecha: 07/08/2025 - 02:43
👨‍💻 Autor: Giancarlo + Tars-90
