# Software Notarios | Checkpoint 02/08/2025

## 📌 Estado Actual

- **Versión estable recuperada**: Commit `e4fe265`  
  - 🎨 Dashboard funcional básico (sin colores ni estilos finales).  
  - ✅ BDD inicializada correctamente con **13 tablas**.  
  - 🚀 Proyecto levanta sin errores con `flask run`.  

- **Rama de trabajo actual:** `stable/recovery_0208`  
- **Dependencias:** Reinstaladas y limpias, sin `__pycache__`.  
- **Seeds:** Pendiente de verificar `flask seed-cli init` para creación de SuperAdmin y Bufete principal.

---

## 🗂️ Estructura funcional confirmada

1. **Dashboard básico:**  
   - Navbar operativo  
   - Plantillas `base.html` y `dashboard.html` funcionando  

2. **Base de datos (13 tablas):**  
   - Bufetes, Usuarios, Notarios, Procuradores, Asistentes  
   - Documentos notariales y librería inicial  
   - Tablas de auditoría en diseño pendiente  

---

## 🎯 Próximos Pasos

1. **Confirmar Seeds**  
   ```bash
   flask seed-cli init
