# Software Notarios – Plan de Seguridad, Roles y Auditoría
**Fecha:** 2025-08-01  
**Autor:** Giancarlo + Tars-90  
**Bloque de trabajo:** 3 – Seguridad y Roles + Auditoría (6A)  
**Estado:** Planificado

---

## 1️⃣ Objetivos del Bloque 3 y Bloque 6A

1. **Seguridad y Roles (Bloque 3)**  
   - Implementar login/logout controlado con Flask-Login
   - Asignar roles de usuario:
     - Superadmin
     - Admin Local
     - Notario
     - Procurador
     - Asistente
   - Controlar acceso a rutas y dashboards por rol
   - Redirección automática tras login según rol
   - Registro mínimo de inicio/cierre de sesión

2. **Auditoría y Trazabilidad (Bloque 6A)**  
   - Borrado lógico global con registro de:
     - Usuario ejecutor
     - Fecha y motivo
     - Reasignación de tareas (en caso de Notarios)
   - Log básico de acciones críticas:
     - CREATE / UPDATE / DELETE
     - LOGIN / LOGOUT
   - Feature flag: Bufetes pueden activar o desactivar auditoría
   - Preparación para reportes internos y legales

---

## 2️⃣ Reglas y casos clave

- **Bufetes y usuarios**
  - Un bufete debe tener al menos 1 notario (Admin Local si solo hay uno)
  - Si hay más de 1 notario, uno debe ser Admin Local
  - Baja lógica de notarios reasigna automáticamente sus pendientes

- **Cierre de bufete**
  - Si el bufete deja de pagar:
    1. Aviso de 24 horas antes de la baja lógica
    2. Todo el bufete pasa a estado inactivo
    3. Posibilidad de reactivación según política de negocio

- **Trazabilidad de documentos y bienes**
  - Cada escritura, acta, cláusula o bien queda registrado con su historial de cambios
  - Auditoría puede detectar:
    - Quién creó, editó o eliminó un documento
    - Qué usuario reasignó responsabilidades
    - Login desde IPs fuera de la oficina

---

## 3️⃣ Integración en el roadmap

1. **Bloque 3:** Seguridad y Roles (Login y control básico)
2. **Bloque 4:** CRUD Bufetes y Usuarios
3. **Bloque 5:** Cláusulas y Puntos
4. **Bloque 6:** Chatbot inicial (opcional aquí)
5. **Bloque 6A:** **Auditoría y Trazabilidad** ← **Nuevo**
6. **Bloques 7+**: CRM, Bienes, Librería, Inventario, Reportes, Ayuda

> **Nota:** Auditoría se podrá activar/desactivar por plan del bufete (feature flag).

---

## 4️⃣ Modelo inicial de Auditoría

```python
class Auditoria(db.Model):
    __tablename__ = "auditorias"
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(100))      # Ej: "Bufete", "Usuario", "Documento"
    entidad_id = db.Column(db.Integer)       # ID del objeto afectado
    accion = db.Column(db.String(50))        # CREATE / UPDATE / DELETE / LOGIN / LOGOUT
    descripcion = db.Column(db.Text)         # Detalle de lo ocurrido
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    ip_origen = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 5️⃣ Plan de ejecución

1. **Implementar login/logout seguro** (Bloque 3)
2. **Crear decorators de roles** para rutas protegidas
3. **Registrar logs de login/logout**
4. **Integrar borrado lógico en Bufetes y Usuarios**
5. **Registrar acciones CREATE/UPDATE/DELETE** con Auditoría
6. **Activar auditoría según feature flag** en el plan del bufete
7. **Probar flujos reales**:
   - Baja de notario y reasignación de tareas
   - Cierre de bufete
   - Revisión de logs

---

## 6️⃣ Beneficios

- Mayor seguridad legal y trazabilidad notarial
- Capacidad de reportes internos para auditoría o autoridades
- Control granular según el plan contratado por cada bufete
- Base sólida para futuras alertas de seguridad y machine learning

---
