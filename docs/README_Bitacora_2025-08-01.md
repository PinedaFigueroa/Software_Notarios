# Bitácora Técnica – 2025-08-01
**Proyecto:** Software Notarios  
**Autor:** Giancarlo + Tars-90  
**Bloque trabajado:** 2 – Dashboard y Blueprints  
**Estado:** Completado ✅

---

## 📌 Resumen de actividades
1. **Finalización de Bloque 2**
   - Dashboard profesional con:
     - Navbar con `logo.png`
     - Cards con métricas de usuarios, documentos, asociaciones
     - Íconos FontAwesome y colores profesionales
     - Tarjeta amarilla dinámica para avisos pendientes
   - Archivos finales:
     - `app/templates/base.html`
     - `app/templates/dashboard/dashboard.html`
     - `app/dashboard/routes.py`
     - `app/static/css/styles.css`
     - `app/static/img/logo.png`
     - `docs/README_Bloque2_Final.md`

2. **Documentación con Sphinx**
   - `gen_docs.py` mejorado para incluir:
     - Todos los `.md` diarios y de bloques
     - `modulos/*` y `source/*` en el `toctree`
   - Generación de HTML exitosa con `sphinx_rtd_theme`
   - Warnings `[toc.not_included]` identificados y plan para reducción en Bloque 3

3. **Control de versiones (Git)**
   - `.gitignore` corregido para ignorar `_build/` y archivos temporales
   - Limpieza de repositorio con `git rm --cached`
   - Commit final y `git push` con Bloque 2 estable

---

## ⚠️ Lecciones de los errores
1. **Warnings de Sphinx**
   - Causados por Markdown sin título o `.rst` fuera del toctree
2. **`git add .`**
   - Subió archivos no deseados hasta que `.gitignore` fue corregido
3. **`make clean` en Windows**
   - Falló por archivos bloqueados en `_build/doctrees`  
   - Solución: borrar manualmente o usar `rmdir /s /q`

---

## ✅ Estado final del día
- Bloque 2 funcional y documentado
- Repositorio limpio y organizado
- Documentación en HTML generada correctamente

---

## 🔮 Pendientes para mañana (Bloque 3)
1. Subpáginas para **Usuarios** y **Documentos**
2. Dashboard de **Superadmin**
3. Primera integración real de **tabla Avisos**
4. Reducción de warnings de Sphinx a <50
5. Integración de `gen_docs.py` con flujo de CI/CD (opcional)

---
