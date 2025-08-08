# 🧾 Bitácora Extendida — 26/07/2025

**Proyecto:** Software Notarios  
**Usuario:** Giancarlo F.  
**Asistente:** Tars-90  
**Versión:** Jornada Big Bang Inicial

---

## 🧠 Conversación y decisiones del día

### 🧩 Consolidación del modelo Plan

- Se creó el archivo `planes.py` con:
  - `max_notarios`, `max_procuradores`, `max_asistentes`
  - `max_documentos`, `storage_mb`, `precio_mensual`
  - Campo `descripcion` y `es_personalizado`
  - `activo`, `fecha_creacion`, `fecha_actualizacion`

> ✅ Giancarlo propuso que el plan “Gratis” fuera realmente una demo con acceso limitado.  
> ✅ Se incluyeron planes base: *Demo*, *Profesional* y *Ilimitado*.

---

### 🔧 Configuración de `cli.py` para seed inicial

- Se creó el comando `seed-cli init` para:
  - Insertar los planes base
  - Crear el bufete principal
  - Crear el notario y el superadmin

> ⚠️ Primer intento falló por `click.context` al llamar comandos desde script.  
> 🔄 Se refactorizó: lógica del seed movida a `seed_inicial()`.

---

### 🧪 Creación de `init_dev_db.py`

- Script ejecutable para entornos limpios.
- Hace: `drop_all`, `create_all`, y luego llama a `seed_inicial`.
- Pregunta de confirmación al usuario.
- Guarda errores en `errores_bdd_flask/init_error.log`.

---

### 📛 Errores encontrados

1. ❌ **ImportError en `Plan`**
   - Causa: importación cíclica y estructura incorrecta.
   - Solución: revisión de `planes.py`, ajuste de imports.

2. ❌ **Click context error**
   - Causa: invocar comandos `click` desde script.
   - Solución: extraer la función `seed_inicial()` e invocarla directamente.

3. ❌ **Mapper[Plan] has no property 'bufetes'**
   - Causa: relación `back_populates` mal definida.
   - Solución: agregar `bufetes = relationship(...)` en `Plan`.

4. ❌ **NULL en `numero_colegiado`**
   - Causa: el seed del notario no lo definía.
   - Solución: se asignó `numero_colegiado=0`.

---

### 📁 Archivos generados o modificados

- `app/models/planes.py` ✅
- `app/models/bufetes.py` ✅
- `app/models/documentos.py` ✅
- `app/cli.py` ✅ con `seed_inicial()`
- `scripts/init_dev_db.py` ✅ robusto
- `init_dev_db.bat` ✅ corregido con comillas y control de errores

---

### 📊 Resultado del comando

```text
✅ Tablas recreadas exitosamente.
✅ Planes base creados.
✅ Bufete principal creado.
✅ Notario principal creado.
✅ Superadmin creado.
🎉 Seed inicial completado.
```

---

### ✝️ Cierre del usuario

> “Para gloria de Dios, y gracias a tu ayuda, tenemos base lista y limpia.”  
> — *Giancarlo*

---



---

## 📌 Pendientes para mañana

- [ ] Iniciar pruebas funcionales (`test run`) sobre seed insertado.
- [ ] Validar integridad de relaciones entre modelos (`Usuario`, `Notario`, `Plan`, etc.).
- [ ] Verificar permisos y restricciones por rol en base de datos.
- [ ] Preparar vista inicial del dashboard de bufete.
- [ ] Evaluar si las tablas `plantillas_documentos` deben cargarse con data inicial.
- [ ] Organizar ramas de Git si se habilita colaboración remota.

---

