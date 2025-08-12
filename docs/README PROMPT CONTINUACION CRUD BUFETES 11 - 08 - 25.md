# Proyecto: Software Notarios CRUD BUFETES 11 - 08 - 25

## Fecha: 11/08/2025

## Objetivo de esta sesión

Continuar desarrollo del **Panel de Control del SuperAdmin** y CRUD de **Bufetes** y **Usuarios**. El sistema ya cuenta con login funcional y redirección por rol. Vamos a enfocar en:

1. Listado de bufetes con opciones de **editar** y **eliminar**.
2. Poder **crear** bufetes desde el panel.
3. Revisar y completar CRUD de usuarios.

---

### Estado actual (11/08/25)

#### ✅ Funcional

* **Login**: Operativo. Redirige al dashboard correcto según rol.
* **Dashboard del SuperAdmin**:

  * Muestra métricas principales: Bufetes registrados, usuarios totales, superadmins, espacio usado.
  * Botones a "Bufetes" y "Usuarios" (plantillas listas).
* **Botón de Bufetes**:

  * Lleva a `/superadmin/bufetes` (pantalla lista, pero sin datos ni iconos de acción aún).
* **Paleta de colores**: El panel general sí tiene colores; el de SuperAdmin mantiene estilo limpio.

#### ⚠ Pendiente

1. **Botón de Usuarios**: No funcional, falta implementación de ruta/listado.
2. **Listado de bufetes**:

   * No muestra datos existentes.
   * Falta implementar iconos y acciones (editar/eliminar).
3. **Agregar bufete**: Falta conectar el botón **+ Nuevo Bufete** con el formulario y la lógica en `routes_bufetes.py`.
4. **CRUD de usuarios**: Falta implementación completa.

---

### Archivos disponibles para el módulo SuperAdmin:

**Estructura de carpetas y archivos**

```
app/superadmin/
    __init__.py
    forms_bufetes.py
    forms_usuarios.py
    routes.py
    routes_bufetes.py
    routes_usuarios.py
    templates/
        superadmin/
            dashboard.html
            bufetes/
                form_bufete.html
                listar_bufetes.html
            usuarios/
                form_usuario.html
                listar_usuarios.html
```

---

### Lo que necesito que revisemos de inmediato (incisos para pedirte en la nueva pestaña):

1. **`routes_bufetes.py`** → Confirmar si está consultando correctamente `BufeteJuridico.query.all()` y pasando datos a `listar_bufetes.html`.
2. **`listar_bufetes.html`** → Incluir tabla con bucles de Jinja para mostrar todos los bufetes, con columnas ID, nombre, plan, activo, y **acciones** (editar/eliminar).
3. **`routes_usuarios.py`** → Revisar si existe listado y CRUD, o crear desde cero.
4. **Navbar en login** → Ajustar para que en la pantalla de login no se muestre el navbar completo (solo logo).

---

### Propuesta de avance para hoy:

1. **Listar bufetes con datos reales** y añadir iconos de acciones.
2. **Formulario de nuevo bufete** enlazado al botón + Nuevo Bufete.
3. Preparar **CRUD de usuarios** de forma similar.

---

¿Quieres que te pase ahora mismo el contenido actual de `routes_bufetes.py` y `listar_bufetes.html` para ajustarlos?
Con eso resolvemos el listado hoy mismo y dejamos el CRUD funcional.
