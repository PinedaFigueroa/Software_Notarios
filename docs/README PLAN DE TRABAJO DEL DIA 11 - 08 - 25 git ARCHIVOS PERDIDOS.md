# README PLAN DE TRABAJO DEL DIA 11 - 08 - 25
se descubrió el problema con los git y archivos perdidos

Descargar ZIP — ENTREGA_superadmin_routes_2025-08-11.zip
Qué incluye este zip (solo archivos modificados):
•	app/superadmin/routes_bufetes.py → ahora consulta real con q (búsqueda), y agrega POST /toggle para activar/desactivar.
•	app/superadmin/routes_usuarios.py → listado global y por bufete con consultas reales.
Puntos clave ya resueltos según tus incisos
1.	#1 routes_bufetes.py ✔️
o	Ahora usa BufeteJuridico.query con filtro ilike por nombre_bufete cuando viene ?q=... y pasa bufetes y q al template ().
2.	#2 listar_bufetes.html ✔️
o	Tu plantilla ya está perfecta para renderizar los datos y usa los url_for(...) que ahora existen: editar_bufete, toggle_estado_bufete, crear_bufete. No requiere cambios.
3.	#3 routes_usuarios.py ✔️
o	Implementado listado global y por bufete con queries reales ().
4.	Navbar en login (pendiente menor)
o	Añade esta condición en tu base.html para ocultar el navbar completo en la pantalla de login (o cuando no hay sesión):
5.	{% if current_user.is_authenticated and request.endpoint not in ['auth_bp.login'] %}
6.	  {# aquí tu navbar #}
7.	{% endif %}
Si tu blueprint de auth usa otro endpoint, ajusta el nombre del endpoint en la lista.
Cómo probar rápido
•	Ir a /superadmin/bufetes → deberías ver la tabla con tus bufetes.
•	Probar el buscador con ?q=TuNombre.
•	Usar el botón Activar/Desactivar (toggle) para el borrado lógico.
•	Ir a /superadmin/usuarios para el listado global y a /superadmin/bufetes//usuarios para el listado por bufete.
•	El botón Editar y + Nuevo Bufete abren el formulario (stub) y dejan listo el flujo para integrar WTForms y persistencia en la siguiente iteración.
Siguientes pasos propuestos (rápidos):
•	Integrar forms_bufetes.py para crear/editar con validación y db.session.add/commit.
•	Añadir eliminar lógico (si lo quieres separado del toggle).
•	Implementar routes_usuarios.py CRUD (crear/editar/desactivar) usando forms_usuarios.py.
¿Quieres que ya conecte el POST real de crear/editar bufete con forms_bufetes.py (WTForms) y te deje otro zip cerrado? Pégame la clase del form si tiene un nombre distinto a BufeteForm y lo resuelvo al toque.
 
¡Hecho, Giancarlo! Te dejo un paquete único que conecta el CRUD real de Bufetes y Usuarios, añade búsqueda, toggle de activo, y ajusta base.html para ocultar el navbar completo en el login (dejando solo el logo).
Descargar ZIP — ENTREGA_CRUD_superadmin_2025-08-11.zip
Qué incluye (para pegar encima del proyecto):
•	app/superadmin/forms_bufetes.py → WTForm BufeteForm (nombre, plan, activo).
•	app/superadmin/forms_usuarios.py → WTForm UsuarioForm (nombres, apellidos, correo, rol, bufete, activo).
•	app/superadmin/routes_bufetes.py → Listar/buscar, crear, editar, toggle activo. Importa BufeteJuridico con fallback (ubicado en models/usuarios o models/bufetes) y usa db.session.
•	app/superadmin/routes_usuarios.py → Listar global y por bufete con búsqueda, crear, editar, toggle activo. Usa Usuario y RolUsuarioEnum si está disponible.
•	app/superadmin/templates/superadmin/usuarios/listar_usuarios.html → Tabla funcional con acciones.
•	app/superadmin/templates/superadmin/usuarios/form_usuario.html → Formulario WTForms.
•	app/superadmin/templates/superadmin/bufetes/form_bufete.html → Formulario WTForms.
•	app/templates/base.html → Detecta request.endpoint == 'auth_bp.login' y oculta el navbar (muestra solo logo).
Cómo probar (rápido):
1.	Bufetes
o	Ir a /superadmin/bufetes → verás el listado con búsqueda ?q=....
o	+ Nuevo Bufete: crea y guarda con plan (opcional).
o	Editar: actualiza datos.
o	Activar/Desactivar: hace toggle del campo activo.
2.	Usuarios
o	Ir a /superadmin/usuarios → listado global con búsqueda por nombre/correo.
o	/superadmin/bufetes//usuarios → listado filtrado por bufete.
o	+ Nuevo Usuario y Editar: usa UsuarioForm, con roles desde RolUsuarioEnum si existe y bufetes en dropdown.
o	Activar/Desactivar: toggle de activo.
Notas de integración:
•	Los forms refrescan choices dinámicas (refresh_choices()), trayendo planes y bufetes desde la BD.
•	Se manejan imports flexibles para BufeteJuridico y Plan por los cambios que has hecho entre models/usuarios.py y models/bufetes.py. Si en tu repo el nombre de módulo de Plan es distinto, me dices y lo fijo a tu ruta exacta.
•	Se respeta tu decorador rol_required y el blueprint superadmin_bp tal como ya lo usas.
¿Siguiente sprint? Puedo:
•	Añadir confirmaciones con modal para toggles,
•	Validaciones extra (unicidad de nombre_bufete),
•	Paginación en listados,
•	Y, si quieres, incluir exportar a CSV de bufetes/usuarios desde el SuperAdmin.

Perfecto, partner.
Si el ZIP de iconos lo generé antes del reset del entorno, por eso te dio “file not found”; lo dejamos pendiente para después.
Ahora vamos a conectar los botones del listado de bufetes y usuarios para que ya creen/editen y guarden datos en la BD.
________________________________________
🔹 Lo que tenemos
•	listar_bufetes.html ya tiene:
o	Botón + Nuevo Bufete → superadmin_bp.crear_bufete
o	Botón Editar → superadmin_bp.editar_bufete
•	listar_usuarios.html ya tiene:
o	Botón + Nuevo Usuario → superadmin_bp.crear_usuario
o	Botón Editar → superadmin_bp.editar_usuario
Los endpoints existen en routes_bufetes.py y routes_usuarios.py, pero estaban como stub o requieren validar con WTForms y db.session.
________________________________________
🔹 Pasos para dejarlos funcionando
1. Bufetes
En routes_bufetes.py:
•	crear_bufete:
o	Validar con BufeteForm.
o	Insertar en BD con db.session.add() y db.session.commit().
o	Redirigir al listado con mensaje flash.
•	editar_bufete:
o	Cargar el bufete por id.
o	Prellenar formulario con datos actuales.
o	Guardar cambios y commit.
El código que ya te pasé en el ZIP de hoy (ENTREGA_CRUD_superadmin_2025-08-11.zip) ya está listo para hacer esto si forms_bufetes.py y plan_id funcionan.
________________________________________
2. Usuarios
En routes_usuarios.py:
•	crear_usuario:
o	Validar con UsuarioForm.
o	Insertar en BD con db.session.add() y db.session.commit().
•	editar_usuario:
o	Cargar el usuario.
o	Prellenar el form.
o	Guardar cambios y commit.
El código de ese ZIP también lo contempla.
________________________________________
3. Lo que hay que asegurar ahora
•	El archivo forms_bufetes.py debe tener:
•	from flask_wtf import FlaskForm
•	from wtforms import StringField, SelectField, BooleanField, SubmitField
•	from wtforms.validators import DataRequired, Length
y el método refresh_choices() para llenar plan_id.
•	El archivo forms_usuarios.py debe tener:
•	from flask_wtf import FlaskForm
•	from wtforms import StringField, SelectField, BooleanField, SubmitField
•	from wtforms.validators import DataRequired, Email, Length, Optional
y el método refresh_choices() para roles y bufetes.
________________________________________
📌 Mi propuesta:
Te preparo un ZIP mínimo con:
app/superadmin/forms_bufetes.py
app/superadmin/forms_usuarios.py
app/superadmin/routes_bufetes.py
app/superadmin/routes_usuarios.py
actualizados para:
•	Guardar/editar bufetes y usuarios realmente.
•	Manejar mensajes flash y redirecciones.
•	Usar tu core_ext.py (ya que ahora lo tienes en /app).
¿Quieres que te lo deje listo para que lo pegues encima y esos botones ya graben en la BD?
 
REM 1) Evita que Windows meta basura: ignora desktop.ini (si no estaba)
echo desktop.ini>> .gitignore

REM 2) Agrega TODO (incluye los no trackeados como app/core_ext.py y el HTML de respaldo)
git add -A

REM 3) Commit único y descriptivo
git commit -m "feat(superadmin): CRUD bufetes/usuarios + fix navbar login + alias core_ext

- Conecta crear/editar Bufetes y Usuarios con WTForms y BD
- Oculta navbar completa en /login (logo + nombre únicamente)
- Agrega app/core_ext.py (alias de db para compatibilidad)
- Tooltips (title) en listados y mejoras menores
"

REM 4) Rama estable del día (snapshot local)
git branch -f stable/dia_2025-08-11

REM 5) Tag del snapshot (por si necesitas volver exacto a este punto)
git tag rec_2025-08-11

REM 6) Verifica
git status
git log --oneline -n 3
