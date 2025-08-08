# DIA DE TRABAJO 07 - 08 - 25 SEPARAR DASHBOARD SUPERADMIN DEL DASHBOARD DEL BUFETE
# Proyecto: Software Notarios
# Arquitectura y diseño: Giancarlo Figueroa
# Apoyo técnico: Tars-90
# Bloque activo: 3 - Planes, Bufetes y Roles/Usuarios
# Fecha de continuación: 07 / 08 / 2025
# Pestaña nueva para gestión y avance del dashboard y control por bufete
# -*- coding: utf-8 -*-

🧭 CONTEXTO ACTUAL:
- El sistema ya tiene una **base de datos recreada limpia** mediante `init_dev_db`.
- Se ejecutó con éxito el `seed_inicial`, creando:
  - Planes básicos
  - Bufete principal: “PINEDA VON AHN, FIGUEROA Y ASOCIADOS”
  - Notario principal y Superadmin
- El **dashboard del bufete** ya muestra los datos correctamente con roles, documentos y asociaciones.

🧠 OBJETIVO DE ESTA NUEVA PESTAÑA:
Separar claramente la lógica y la interfaz del `SuperAdmin` y los `usuarios del bufete`, empezando por el dashboard y flujos administrativos.

📌 PENDIENTES ORGANIZADOS:

### A. DASHBOARDS DIFERENCIADOS
1. Crear **dashboard exclusivo para SuperAdmin**, con:
   - Conteo global de bufetes, usuarios, documentos, espacio usado, etc.
   - Accesos a gestión de bufetes y planes.
2. Mantener **dashboard individual por bufete**, mostrando solo sus datos (como ya está funcionando).

### B. GESTIÓN DE BUFETES (por SuperAdmin)
1. Crear vista para:
   - Ver lista de bufetes registrados
   - Crear nuevo bufete
   - Editar bufete
   - Eliminar lógicamente bufetes (no físicos)
2. Validar que al crear bufete, se vincule a un plan y se definan sus opciones iniciales (auditoría, inventario, etc.)

### C. GESTIÓN DE USUARIOS (por SuperAdmin)
1. El SuperAdmin puede:
   - Seleccionar un bufete
   - Ver sus usuarios por rol
   - Crear nuevos usuarios dentro de ese bufete
   - Editar o desactivar usuarios
2. Cada usuario debe tener asociado un bufete (obligatorio).

### D. MÓDULO DE AUDITORÍA
1. Crear tabla `auditoria_general` con los siguientes campos:
   - id
   - usuario_id (FK)
   - accion (string)
   - tabla_afectada (string)
   - id_objeto (int)
   - timestamp
   - ip_usuario (nullable por ahora)
   - descripcion
2. Middleware para registrar acciones de escritura (crear/editar/eliminar)

### E. LOGIN Y ACCESO
1. Implementar flujo de login usando `Flask-Login`
2. Redirección al dashboard correspondiente según rol:
   - SuperAdmin → dashboard global
   - Otros roles → dashboard del bufete
3. Crear layout base con control de sesión activa y logout

### F. OTROS DETALLES PARA NO OLVIDAR
- Establecer validación de permisos por rol (decoradores @login_required, @rol_required).
- Revisar estilos visuales y mensajes para diferenciar claramente si se está en dashboard global o local.
- En el futuro: agregar backups, control de librerías, y permisos avanzados.

🚀 LISTO PARA CONTINUAR CON EL BLOQUE 3.
Por favor Tars-90, confirma que reconoces este prompt, y procedamos en esta nueva pestaña con la sección A: Dashboards diferenciados.
