# Bloque 1 – Problemas con el Big Bang & Seed Inicial

**Fecha de finalización:** 31/07/2025 14:50\
**Responsable:** Giancarlo + Tars-90

---

## ✅ Avances

1. **Base de datos **`` recreada correctamente usando `init_big_bang.py`.
2. **Migraciones Alembic** aplicadas con éxito (migración inicial `big_bang_initial_creation.py`).
3. **Seed inicial ejecutado** sin errores:
   - Usuarios creados: `admin`, `notario_demo`, `admin_local`, `notario_pineda`
   - 23 cláusulas iniciales insertadas en `ClausulasPuntos`
4. **Logs generados con timestamp**: `big_bang_20250731_145012.log`
5. **Verificación con Flask Shell**:
   ```python
   [u.username for u in Usuario.query.all()]
   # ['notario_pineda', 'admin', 'notario_demo', 'admin_local']

   ClausulasPuntos.query.count()
   # 23
   ```
6. **App probada en navegador** → Interfaz funcional y estable.

---

## 🛠 Errores y Soluciones

1. **ENUM PostgreSQL: **``

   - **Causa:** Se insertaba `rol='notario'` en minúsculas
   - **Solución:** Usar `RolUsuarioEnum.NOTARIO.name` (mayúsculas)

2. **Tabla **``** no existía**

   - **Causa:** Migración inicial no incluía modelo
   - **Solución:** Asegurar importación en `models/__init__.py` y regenerar migración

3. **Problemas con rutas con espacios en Windows**

   - **Solución:** Modo híbrido Python + `.bat` y logs con timestamp

---

## 📌 Pendientes para el siguiente bloque

1. Diseñar **Dashboard** del bufete y **blueprints**.
2. Probar `scripts/test_relaciones_asociacion.py` para relaciones Notario-Procurador.
3. Implementar **generación automática de README diario** en cada Big Bang.
4. Primer commit Git del proyecto consolidado.

---

## 🔹 Nota sobre UX para Notarios

- Se abrirá investigación en Bloque 3 para identificar:
  1. **Puntos de dolor** que hacen que notarios eviten cierto software.
  2. **Colores y diseño visual** que generen comodidad y atracción.
  3. **Sustento psicológico y estudios de usabilidad** aplicados a software legal/notarial.

---

**Estado:** ✅ **Bloque 1 completado** – Listo para continuar con Dashboard y Blueprints

