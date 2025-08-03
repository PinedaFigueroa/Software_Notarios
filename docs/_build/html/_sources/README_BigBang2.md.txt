# 📝 Big Bang 2 – Proceso de (RE) Inicialización de Base de Datos

## 1. Contexto

El proceso **Big Bang 2** se diseñó para reinicializar la base de datos de desarrollo
del proyecto **Software Notarios** de manera **segura, trazable y reproducible**.

### Evolución de versiones

- **v2** → Primer intento en Python, inspirado en `init_dev_db.bat`  
- **v3** → Agregó tracking y logs paso a paso  
- **v4** → Manejo de decisiones (S/N) y logs de auditoría  
- **v5** → Versión híbrida y definitiva:
  - `.bat` oficial para Windows (probado y confiable)  
  - `.py` híbrido que usa el `.bat` si hay rutas con espacios

---

## 2. Problemas históricos solucionados

1. **Errores de codificación (`UnicodeDecodeError`)**  
   - Ocurrían por rutas con espacios (`Mi unidad`) en Windows  
   - Se solucionó usando el `.bat` para evitar `psycopg2` en esa fase

2. **Conflictos de collate / encoding**  
   - Evitados creando la base con:
     - `template0`
     - `UTF8`
     - `LC_COLLATE='C'` y `LC_CTYPE='C'`

3. **Operadores sin guía clara**  
   - Se implementó tracking paso a paso en consola y logs

4. **Múltiples pruebas dejaban residuos de migraciones**  
   - Se agregó limpieza automática de `migrations/versions`

---

## 3. Logs y Auditoría

Todos los errores y decisiones del operador se registran en:


Ejemplo de log (`big_bang_2_v5.log`):
[2025-07-29 20:05:13] La base de datos "software_notarios_dev" EXISTE.
[2025-07-29 20:05:13] Operador respondió 's'. Se eliminará y recreará la base.
[2025-07-29 20:05:15] ✅ Base creada correctamente.
[2025-07-29 20:05:20] ✅ Migraciones aplicadas correctamente.
[2025-07-29 20:05:22] ✅ Seed inicial completado correctamente.
[2025-07-29 20:05:23] 🎉 Big Bang 2 v5 completado sin errores.

---

## 4. Recomendaciones

- **Siempre crear la base con `template0`** para evitar errores de collation  
- **Mantener los logs** para auditoría y diagnóstico  
- **Seguir este procedimiento en producción**, nunca crear la DB manualmente desde pgAdmin  
- **Guardar archivos `.bat` sin BOM** para evitar problemas de codificación

---

## 5. Archivos relacionados

- `init_big_bang_2_v5.bat` → Ejecutar en Windows  
- `scripts/init_big_bang_2_v5.py` → Ejecutar en Linux/Mac o CI/CD  
- Logs → `errores_bdd_flask/big_bang_2_v5.log`  

---

## 6. Histórico de mejoras

| Versión | Mejoras clave |
|--------|---------------|
| v2 | Primer script en Python, inspirado en el `.bat` |
| v3 | Tracking paso a paso y logs |
| v4 | Registro de decisiones del operador en logs |
| v5 | Híbrido: usa `.bat` en Windows y Python en rutas seguras |
