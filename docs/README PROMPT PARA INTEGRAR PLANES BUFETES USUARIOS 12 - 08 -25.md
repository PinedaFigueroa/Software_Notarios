# README PROMPT PARA INTEGRAR PLANES BUFETES USUARIOS 12 - 08 -25

al ingresar un bufete, pienso que debería llevar los campos que se tienen en models \bufetes
igualmente, en usuarios.

pero allí nos pedirá que incluyamos planes, por eso se habían creado algunos en el seed, ¿correcto?

 creo que lo mejor es entonces que el superadmin pueda crear planes,  
verlos justamente ahorita seria de suma utilidad, ya se sabría que usar para las pruebas, para ello crear el crud... 

NOTA IMPORTANTE: tenemos el problema de cambiarnos de pestañas, por el tema del performance, y eso hace que se tenga que hacer un refresh, esto conlleva el tema de nombres de variables, endpoints, rutas, estructura de archivos, etc.  POR ESO SE DEBE DEJAR CREADO Y FUNCIONANDO EL CRUD DE PLANES, LUEGO EL DE BUFETES AMARRADO A LOS PLANES, Y LOS USUARIOS QUE SE AGREGUEN AL BUFETE DESEADO.

NOTA SUPER IMPORTANTE. AL CREAR UN USUARIO, ME DESPLEGÓ MUY BONITO PERO LAS OPCIONES INCLUIAN SUPERADMIN… ¿SERÁ QUE EL SUPERADMIN NECESITA CREAR OTRO USUARIO SUPERADMIN, DENTRO DE LOS BUFETES CREADOS? Pienso que no, a nivel general podría ser que si crece mucho la aplicación y la clientela, se necesite otro, y creado por fuera de la aplicación, eso nos evita cualquier riesgo de seguridad

¿Cuál es la visión que se tiene? Que todo aquello por donde se pase, se pruebe, Y DEJARLO NITIDO, NO TENER QUE REGRESAR UNA Y OTRA VEZ,

 seguir la arquitectura con mi VISIÓN, from top to bottom (en las gestiones para cada opción, bufetes, usuarios, etc) , from left to right (dentro del navbar) evitando PERDER ESTETICA, Y TERMINAR CON AMONTONAMIENTOS

otro punto importante: de una vez crear respetando los colores ya establecidos, paleta profesional, para el panel de control se utilizó azules, y así según los estudios que te pedí que hicieras sobre los colores preferidos por los profesionales del Derecho, o puedes hacerlo nuevamente (dejando rojo, amarillo, para cosas de emergencias, llamar la atención sobre problemas)

el help al pasar el mouse, es importante, desde ya, además de que se vaya creando el help general.

No olvidar que para efectos de auditoria y trazabilidad (quienes lo adquieran) los usuarios deberían ser controlados que se firmen solo dentro de la oficina , y quizás en casos especiales autorizar que se conecten por fuera, por ahora creo que debería quedar restringido. 

Un usuario, un login, en todo el sistema, eso nos protege del mal uso.

Para auditoria, también hablamos que: 

Dado lo vital del trabajo de los Notarios, este modulo debe permitir saber quien hizo qué, con qué archivos, hora y fecha del trabajo. Si bien no todos adquirirán el módulo, posiblemente al inicio, pero si se les explica lo fundamental por auditoria y trazabilidad, casi que seguramente lo adquieren (objetivo del software ayudar y venderse) tiene que estar preparado y funcionando para todos, aunque no lo usen, ¿me explico bien? Creo que es más fácil que se tenga implementado, pero los reportes y los warnings al dashboard, solo llegarán para quien tenga el modulo adquirido, por supuesto al dashboard del superadmin, esto es indispensable que avise (ejemplo: intento de conexión fuera de oficina, o algo así).

Me parece a mi también que vamos a implementar por bufete dentro de la gestión de reportes internos: cuantos documentos se generaron, rechazos, para quien adquiera el modulo de timbres fiscales y papel protocolo, los costos que han representado, que procurador tiene más carga de trabajo (para distribuir) mas errores, mas rechazos, etc. 
 

para que te refresques la memoria, acá van los models

# archivo: app/models/bufetes.py
# fecha de creación: 15 / 07 / 25 hora 09:20
# cantidad de lineas originales: ~40
# ultima actualización:
# motivo de la actualización: modelo principal de bufetes
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Modelo BufeteJuridico:
Representa un bufete con configuración, datos de contacto y feature flags.
"""
# import datetime  # se probará importar todo de core, si funciona quitar estas lineas
# from app import db
# from sqlalchemy.orm import relationship
# from sqlalchemy import Enum, Boolean, ForeignKey, DateTime

from app.models.core import * 
#------------------------
# MODELO: BufeteJuridico
# ------------------------
class BufeteJuridico(db.Model):
    __tablename__ = 'bufetes_juridicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_bufete = db.Column(db.String(255), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    nit = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)

    # Personalización de marca y aplicación SI EN EL FUTURO SE CONCESIONA
    # app_copyright = db.Column(db.String(255), nullable=True)
    # nombre_aplicacion = db.Column(db.String(255), nullable=True)

    # Configuración y permisos para lo que ha elegido
    # feature flags, 
    maneja_inventario_timbres_papel = db.Column(Boolean, default=True, nullable=False)
    incluye_libreria_plantillas_inicial = db.Column(Boolean, default=True, nullable=False)
    habilita_auditoria_borrado_logico = db.Column(Boolean, default=True, nullable=False)
    habilita_dashboard_avanzado = db.Column(Boolean, default=True, nullable=False)
    # esta ayuda deben tenerla todos, se puso acá pero es parte de lo necesario
    habilita_ayuda_contextual = db.Column(Boolean, default=True, nullable=False)
    # esto digital servirá cuando se exporte el sw o cambie la ley en Guatemala
    habilita_papeleria_digital = db.Column(Boolean, default=True, nullable=False)
    
    # este campo hizo falta en determinado momento, como contactar al bufete
    forma_contacto = db.Column(db.String(255), nullable=True)

    # Facturación por uso de la apliación
    facturacion_nombre = db.Column(db.String(255), nullable=True)
    facturacion_nit = db.Column(db.String(50), nullable=True)
    facturacion_direccion = db.Column(db.String(255), nullable=True)

    # Métodos de pago del bufete
    formas_pago = db.Column(db.String(150), nullable=True)  # ejemplo: "efectivo,tarjeta,transferencia"
    metodo_pago_preferido = db.Column(db.String(50), nullable=True)

    # Control si no ha pagado, si se borra lógicamente
    activo = db.Column(Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
    plan = relationship('Plan', back_populates='bufetes')

    usuarios = relationship('Usuario', back_populates='bufete', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Bufete %s>" % self.nombre_bufete_o_razon_social

 
# archivo: app/models/planes.py
# fecha de creación: 16/07/25 hora 09:50
# cantidad de lineas originales: ~40
# última actualización: 26/07/25 hora 20:10
# motivo de la actualización: corrección de importación, expansión del modelo y preparación para planes base
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

class Plan(db.Model):
    """
    Modelo: Plan

    Representa un plan contratado por un bufete jurídico.

    Campos principales:
    - nombre: Nombre del plan (ej. Demo, Profesional, Ilimitado)
    - descripcion: Breve descripción visible en el dashboard
    - límites: usuarios, documentos, almacenamiento
    - precio_mensual: Costo en quetzales
    - es_personalizado: Bandera para planes fuera del catálogo general
    - activo: Si está disponible para nuevos bufetes
    - fechas: creación y actualización

    Usos:
    - Control de acceso según el plan contratado
    - Facturación y visualización de plan actual
    """
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    max_notarios = Column(Integer, nullable=False, default=1)
    max_procuradores = Column(Integer, nullable=False, default=1)
    max_asistentes = Column(Integer, nullable=False, default=0)
    max_documentos = Column(Integer, nullable=False, default=10)
    storage_mb = Column(Integer, nullable=False, default=100)

    precio_mensual = Column(Float, nullable=False, default=0.0)
    es_personalizado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

    # Auditoría
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    bufetes = relationship("BufeteJuridico", back_populates="plan")

    def es_valido_para(self, notarios, procuradores, asistentes, documentos, uso_mb):
        return (
            notarios <= self.max_notarios and
            procuradores <= self.max_procuradores and
            asistentes <= self.max_asistentes and
            documentos <= self.max_documentos and
            uso_mb <= self.storage_mb
        )

    def __repr__(self):
        return f"<Plan {self.nombre} Q{self.precio_mensual}>"

 
y aquí van USUARIOS. Estoy pensando que debería tener Documento Personal de Identificación, incluido (podríamos agregarlo al usuario base, me parece) por ahora dejarlo como opcional, y en el momento que sea obligatorio cumplir con las validaciones, ya explicadas en otro chate, según lo hace la librería de Python.

# archivo: app/models/usuarios.py
# fecha de creación: 26 / 07 / 25
# cantidad de lineas originales: 123
# última actualización: 27 / 07 / 25 hora 00:46
# motivo de la actualización: Consolidación total de modelos de usuario y bufetes, con soporte multitenancy
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""
Este módulo define el modelo principal de usuarios del sistema notarial multitenant.

Incluye:
- Usuario (abstracto): Base para todos los usuarios.
- Notario: Extiende Usuario, con datos colegiado y firma electrónica.
- Procurador: Extiende Usuario, usado para redacción.
- Asistente: Extiende Usuario, tareas complementarias.

Estos modelos soportan:
- Multitenancy por bufete
- Borrado lógico para auditoría
- Adaptabilidad para exportación a otros países
"""

# archivo: app/models/usuarios.py
# Consolidado por Tars-90 el 26/07/2025
# Contiene los modelos completos de Usuario, Notario, Procurador, Asistente y BufeteJuridico

#import datetime
#from app import db
#from sqlalchemy.orm import relationship
# from sqlalchemy import Enum, Boolean, DateTime, ForeignKey

from app.models.core import * 
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum
from flask_login import UserMixin

# ------------------------
# MODELO: Usuario base
# ------------------------
class Usuario(UserMixin,db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    correo = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(Enum(RolUsuarioEnum), nullable=False)
    estado = db.Column(Enum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO)

    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion_laboral = db.Column(db.String(255), nullable=True)
    preferencia_contacto_red_social = db.Column(db.String(100), nullable=True)

    bufete_id = db.Column(db.Integer, db.ForeignKey('bufetes_juridicos.id'))
    bufete = relationship("BufeteJuridico", back_populates="usuarios")

    # Auditoría y control
    borrado_logico = db.Column(Boolean, default=False)

 # ---- Flask-Login integration ----
    @property
    def is_active(self) -> bool:
        """Requerido por Flask-Login: usuario activo si estado=ACTIVO y no borrado lógicamente."""
        # Activo si estado = ACTIVO y no está borrado lógicamente
        from app.models.enums import EstadoUsuarioEnum
        return (self.estado == EstadoUsuarioEnum.ACTIVO) and (not self.borrado_logico)

    # UserMixin ya implementa: is_authenticated, is_anonymous, get_id()

    def __repr__(self):
        return "<Usuario %s (%s)>" % (self.username, self.rol)

# ------------------------
# MODELO: Notario
# ------------------------
class Notario(Usuario):
    __tablename__ = 'notarios'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    numero_colegiado = db.Column(db.String(20), nullable=False)
    colegiado_activo = db.Column(Boolean, default=True, nullable=False)
    fecha_verificacion = db.Column(db.DateTime, nullable=True)

    firma_electronica_registrada = db.Column(Boolean, default=False)
    proveedor_firma_electronica = db.Column(db.String(100), nullable=True)

# ------------------------
# MODELO: Procurador
# ------------------------
class Procurador(Usuario):
    __tablename__ = 'procuradores'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)

# ------------------------
# MODELO: Asistente
# ------------------------
class Asistente(Usuario):
    __tablename__ = 'asistentes'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)

 
# archivo: app/models/enums.py
# fecha de creación: 14/07/25 hora 20:46
# ultima actualización: 16/07/25
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import enum

class TipoDocumentoEnum(enum.Enum):
    ESCRITURA_PUBLICA = "Escritura Pública"
    ACTA_NOTARIAL = "Acta Notarial"
    AVISO = "Aviso"

class EstadoDocumentoEnum(enum.Enum):
    BORRADOR = "Borrador"
    EN_REVISION = "En Revisión"
    FINALIZADO = "Finalizado"
    ENTREGADO = "Entregado"
    ANULADO = "Anulado"

class EstadoUsuarioEnum(enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    SUSPENDIDO = "Suspendido"

class RolUsuarioEnum(enum.Enum):
    SUPERADMIN = "Superadmin"
    ADMINISTRADOR = "Administrador"
    NOTARIO = "Notario"
    PROCURADOR = "Procurador"
    ASISTENTE = "Asistente"

class TipoClausulaEnum(enum.Enum):
    GENERAL = "General"
    PARTICULAR = "Particular"
    ESPECIFICA = "Específica"
    OTRA = "Otra"

class TipoBienEnum(enum.Enum):
    INMUEBLE = "Inmueble"
    VEHICULO = "Vehículo"
    MUEBLE = "Mueble"
    OTRO = "Otro"

class FormaPagoEnum(enum.Enum):
    EFECTIVO = "Efectivo"
    CHEQUE = "Cheque"
    TARJETA = "Tarjeta de Crédito"

 
# archivo: app/cli.py
# fecha de actualización: 06 / 08 / 25
# motivo de la actualización: corregido uso de "nombre" en vez de "nombre_bufete_o_razon_social"
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

import click
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from app import db
from app.models.bufetes import BufeteJuridico
from app.models.usuarios import Usuario, Notario, Procurador, Asistente
from app.models.planes import Plan
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum

cli = AppGroup('seed-cli')

def seed_inicial():
    print("\n🌱 Iniciando seed inicial...")

    # 1️⃣ Planes base
    planes = [
        ("Demo", "Acceso limitado de prueba", 1, 1, 1, 5, 50, 0.0),
        ("Profesional", "Para bufetes pequeños o en crecimiento", 2, 3, 2, 100, 500, 250.0),
        ("Ilimitado", "Sin límites técnicos", 999, 999, 999, 99999, 100000, 1250.0),
    ]

    for nombre, descripcion, n, p, a, doc, mb, precio in planes:
        if not Plan.query.filter_by(nombre=nombre).first():
            db.session.add(Plan(
                nombre=nombre,
                descripcion=descripcion,
                max_notarios=n,
                max_procuradores=p,
                max_asistentes=a,
                max_documentos=doc,
                storage_mb=mb,
                precio_mensual=precio
            ))
    db.session.commit()
    print("✅ Planes base creados.")

    # 2️⃣ Bufete principal
    bufete = BufeteJuridico.query.filter_by(nombre_bufete="PINEDA VON AHN, FIGUEROA Y ASOCIADOS").first()
    if not bufete:
        bufete = BufeteJuridico(
            nombre_bufete="PINEDA VON AHN, FIGUEROA Y ASOCIADOS",
            direccion="5a avenida 15-45 zona 10",
            telefono="2333-4455",
            nit="CF",
            email="admin@bufete.com",
            forma_contacto="Correo institucional",
            plan_id=Plan.query.filter_by(nombre="Profesional").first().id,
            maneja_inventario_timbres_papel = True,
            incluye_libreria_plantillas_inicial= True,
            habilita_auditoria_borrado_logico= True,
            habilita_dashboard_avanzado= True,
            habilita_ayuda_contextual = True,
            habilita_papeleria_digital = False,
        )
        db.session.add(bufete)
        db.session.commit()
        print("✅ Bufete principal creado.")

    # 3️⃣ Notario principal
    if not Notario.query.filter_by(username="notario_pineda").first():
        db.session.add(Notario(
            username="notario_pineda",
            correo="notario@bufete.com",
            password_hash=generate_password_hash("123456"),
            rol=RolUsuarioEnum.NOTARIO,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id,
            numero_colegiado=0
        ))
        db.session.commit()
        print("✅ Notario principal creado.")

    # 4️⃣ Superadmin
    if not Usuario.query.filter_by(username="superadmin").first():
        db.session.add(Usuario(
            username="superadmin",
            correo="admin@bufete.com",
            password_hash=generate_password_hash("123456"),
            rol=RolUsuarioEnum.SUPERADMIN,
            estado=EstadoUsuarioEnum.ACTIVO,
            bufete_id=bufete.id
        ))
        db.session.commit()
        print("✅ Superadmin creado.")

    print("🎉 Seed inicial completado exitosamente.\n")

@cli.command('init')
def seed_cli():
    """🌱 Ejecuta la función seed_inicial con CLI"""
    seed_inicial()

 
todo fabuloso:

1. en todo bufete 1 Notario debe ser administrador (al menos 1) para que se encargue de labores propias dentro de su bufete. ejemplo el bufete A adquiere el servicio, se le pide que indique el nombre del Notario que tendra además de su rol profesional (Notario) el rol de administrador, Caso especial, bufetes muy grandes que puedan requerir además de un Notario, otra persona, podria ser el jefe de IT.

para Guatemala, creo que la mayoría de bufetes , con 1 administrador estarán muy bien. 

2. para las validaciones de DPI y NIT en Guatemala, utilizar https://pypi.org/project/nit-dpi-validator/ 

3. pregunta filosofica con lo de agregar DPI para usuarios (recordemos que en algún momento futuro, version Beta 9 tendrán modulo completo de RRHH) será buena idea incluirlo desde ya??? en personas - clientes es indispensable.

3.1 y he pensado que tengan todos NIT ya que hoy en Guatemala se ha hecho común, el pedirle a personas que facturen (procuradores o asistentes hacia el bufete, los Notarios caso similar, para areas especializadas, le facturan al bufete)

4. por qué te lo digo? porque sabiendo que usaras la libreria indicada, se puede dejar creado lo de la validación de DPI / NIT de manera global, y solamente invocarla, para no estarla definiendo en cada forma, estoy en la visión correcta?

incluye todo esto en tu respuesta anterior y me generas el documento md para guardarlo bajo \docs, y así aparecerá en la documentación respectiva. 

hagamos esto por favor, 

paso siguiente, hacemos git

paso siguiente, generas el zip crude planes y lo dejo descargado, me encanta la idea del patch para expandir lo necesario, pero no queremos caer en circulos viciosos, lo que sea más rápido, el migrate, y esperando primero Dios no tener loops, de lo contrario hacemos big bang... snif snif

 por la hora no sé si podría hacer todo, pero si queda descargado y listo, puedo avanzar, más rápido, 

ah, y si por favor apeguemonos a COMPLETO, asi no caemos en nombres, variables, etc.
