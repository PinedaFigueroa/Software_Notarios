# Proyecto: Software Notarios
## Bloque 2 – Dashboard y Blueprints (Versión Final)
**Fecha:** 01/08/2025  
**Autor:** Giancarlo + Tars-90

---
**Ubicación:** Este documento forma parte de la carpeta `docs/` del proyecto.

### ✅ Avances de Bloque 2
1. **Dashboard funcional y profesional**:
   - Navbar con **logo.png** desde `app/static/img/logo.png`
   - Cards de métricas con colores profesionales e íconos FontAwesome
   - Tarjeta amarilla dinámica para **Avisos Pendientes** (solo aparece si `> 0`)
2. **Bootstrap local** desde `app/static/bootstrap`
3. **`styles.css`** en `app/static/css` para colores y estilos propios
4. **Validaciones Jinja** para evitar errores de variables no definidas

---

### 📂 Estructura final de archivos
Software_Notarios/
├── app/
├── docs/
│   ├── README LECCIONES DE LOS ERRORES 290725.md
│   ├── README_BLOQUE_1_310725.md
│   ├── README_Bloque2_Final.md   <-- este
│   ├── README_Bloque2_Dashboard.md
│   └── ...
└── README.md (documentación general del proyecto)

---

### ⚙️ Pasos de verificación

1. Ejecutar `flask run`  
2. Abrir `http://127.0.0.1:5000/dashboard`  
3. Confirmar:
   - Navbar con **logo.png**
   - Cards de métricas correctas e íconos visibles
   - Tarjeta amarilla de **Avisos Pendientes** aparece solo si `avisos_pendientes > 0`

---

### 📝 Pendientes para Bloque 3
1. Subpáginas para **Usuarios** y **Documentos**
2. Dashboard del **Superadmin** con visión global
3. Implementación real de la tabla **Avisos** y su dash
4. Breadcrumbs y footer corporativo
5. Exportaciones y reportes básicos

---

### 💾 Commit Git sugerido

```bash
git add app/templates/base.html
git add app/templates/dashboard/dashboard.html
git add app/dashboard/routes.py
git add app/static/css/styles.css
git add README_Bloque2_Final.md
git add app/static/img/logo.png

git commit -m "feat(dashboard): Finalización de Bloque 2 - Dashboard completo y estable"
git push origin main

