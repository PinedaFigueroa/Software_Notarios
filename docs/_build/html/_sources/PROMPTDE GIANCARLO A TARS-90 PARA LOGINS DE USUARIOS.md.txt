# PROMPTDE GIANCARLO A TARS-90  PARA LOGINS 070825

tiempo tiempo
rewind 
se crearon usuarios en cli, solamente para tener con que arrancar, 
ahora estamos separando dashboard del bufete principal, del superadmin, este último hace login y tendrá su dash, con la opción de trabajar directo en algún bufete,. lo que corresponde obvio

¿qué necesitábamos para que todo esto funcione?
1. que superadmin pueda crear bufetes
2. para eso tiene que haber creado planes (como un help pusimos en el seed algo de esto, para poder arrancar y probar)
3. si ya hay planes, y pudo crear uno o más bufetes, 
4 a cada bufete, según su plan se le crearan usuarios, pero todos los bufetes, obligatoriamente tienen AL MENOS 1 Notario, los demás roles no son vitales, por razones obvias
5. para pruebas, sin duda crearemos procurador, asistente, 

¿En dónde estamos ahorita?

un dashboard del superadmin, ok, aceptable, 
necesitamos un login, por lo expuesto, pero no pedirá correo sino el username asignado
en este momento la idea posible es que se siga alguna regla como 
Bx_N(P)(A)y_username
En dónde B corresponde al número de bufete
N para notarios, P para procuradores, A para asistentes...

Acá te había pedido ayudas y sugerencias, para el tema de actividades profesionales, el software será usado por oficinas, de profesionales del Derecho, y no sé si hay estándares para este asunto de los usernames, y que se vea mal usar B3_N1_jbenitez..

En otra instancia de pensamiento, esto al principio es sencillo, pero si pasa de cierto número de usuarios el superadmin, empezará a repetir y cometer errores, por lo que lo ideal sería que el proceso fuera:
-	Ingresa el superadmin a su dashboard,
-	Elige gestión de bufetes,
-	Le aparece el listado o las opciones: listado, agregar, editar, eliminar, etc.
-	Crea un nuevo bufete

-	Posteriormente ingresa a la gestión de usuarios (separado del bufete, porque si se deja uno a continuación del otro, se volverá complicado, un error, y a repetir y regresar, además los usuarios se administran con sus particularidades)
-	Lo mismo listar, crear, editar, eliminar… eligirá crear
DESPUES DE INGRESAR LOS DATOS QUE LA PANTALLA LE PIDE, Y CON TODO VALIDADO BIEN, AL DAR EL GUARDAR / SAVE que el sistema genere el username con las combinaciones apropiadas…

En ese sentido, se procedería así:
-	Obligatorio para todo bufete, crear un Notario (¿seria aconsejable hacerlo obligatorio cuando se creó el Bufete, con un aviso, Bufete creado exitosamente, ¿tiene que crear un Notario?  Podría darse el caso que paguen por el servicio, pero no tienen los datos a la mano, y los pasan después, y esto se complicaría entonces. think 
-	Procede a crear procurador(es) asistente(s)
-	Listo ya hay un bufete nuevo, con sus usuarios creados
-	
AHORA ENTENDAMOS BIEN EL TEMA DEL USUARIO:

al ingresarlo llevarán los datos generales que aparecen en las tablas de la bdd, en el caso del notario, número de colegiado (no puede estar en blanco, ser menor a cero, solamente números) , este número no puede estar repetido dentro del bufete (un Notario solamente puede estar registrado 1 vez en el bufete)
NOTA IMPORTANTE: 1 USUARIO SOLO PUEDE ESTAR REGISTRADO 1 SOLA VEZ EN TODO EL SISTEMA, DE LO CONTRARIO PAGARÍAN POR 1 USER Y PODRÍAN UTILIZAR EL SISTEMA N USUARIOS… de darse estos intentos, debe generarse avisos dentro del bufete, warnings, y avisos al superadmin en su dashboard… auditoria

Para quienes paguen el modulo de auditoria, es necesario controlar a los usuarios sus horarios, lo que hicieron, si se conectaron (en caso que se les permita hacerlo ) fuera de la oficina, ese modulo será de mucha ayuda por lo vital que son los documentos y los datos que un Notario maneja. A esto necesito que le pongas tus mejores pensamientos. 

el NIT del notario, los notarios pueden facturarle a ese bufete en el cual están asignados, para eso serviría, en el tema que estamos integrando cosas adicionales como controles de gastos (versión Beta 3)

si se ingresa el NIT (pueden dejarlo en blanco) debe pasar por la revisión que proporciona y ayuda la siguiente 

https://pypi.org/project/NIT-dpi-validator/

al revisar estas líneas y pensando las cosas, me doy cuenta de que no tenemos el campo DPI, documento personal de identificación en Guatemala, habrá que agregarlo a las tablas,

reglas: 
¿pueden dejar el campo DPI en blanco? por ahora si, pero 
si llenan el campo DPI deberá ser validado con la librería que ya indiqué líneas arriba,

por temas legales de Guatemala, hay un impase, así que algunos podrían ingresar como NIT el mismo DPI… para la misma persona… caso muy raro pero si finalmente cambia la ley hacia eso irá todo

el NIT, una vez ingresado y que sea válido según las reglas que la misma librería establece, no puede ser duplicado en el mismo bufete (no hay 2 personas con el mismo NIT) 

nuevamente el Notario podría dar servicios en otro bufete, por lo que su NIT se registraría allí también

en las platicas iniciales contigo (que lastimosamente se pierden) esto del DPI en Guatemala , por el hecho de querer eventualmente exportar el software a Latinoamérica, se debería dejar contemplado de una manera fácil, por ejemplo, si se usará en Salvador, allí el documento personal de identificación se llama xxxx y se valida yyyyy , no sé como podrías ayudarme con esto. Igualmente sería el tema del NIT, se ha buscado pensar en la aplicación para Guatemala y que sea lo más fácilmente exportable a toda LA ya que el notariado es muy parecido. 


HELP CONSTANTE
Se habló en su momento que se tendría un help, para el usuario final, para que al pasar el mouse, hacer hover, sobre los campos, recibiera una ayuda, un mensaje sobre que debe colocar allí… para todos todos los usuarios , y todos los menús sub menús… gestiones etc. 

A su vez se necesitaría ir creando un help=manual del usuario final, que pueda ser una opción en el navbar… 






