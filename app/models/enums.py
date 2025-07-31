# archivo: app/models/enums.py
# fecha de creación: 14 / 07 / 25
# cantidad de líneas originales: ~80
# última actualización: 29 / 07 / 25 hora 13:10
# motivo de la actualización: Enums consolidados para toda la app (usuarios, documentos, bienes, timbres, clausulas, etc.)
# autor: Giancarlo F. + Tars-90
# -*- coding: utf-8 -*-

"""
Este archivo centraliza TODOS los Enum usados en la aplicación Software Notarios.
Objetivos:
1. Evitar errores de ImportError en los modelos
2. Mantener consistencia de valores en la base de datos
3. Facilitar futuras migraciones y mantenimiento
"""

import enum

# ------------------------
# ROLES Y USUARIOS
# ------------------------
class RolUsuarioEnum(enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN_LOCAL = "admin_local"
    NOTARIO = "notario"
    PROCURADOR = "procurador"
    ASISTENTE = "asistente"

class EstadoUsuarioEnum(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    BLOQUEADO = "bloqueado"

# ------------------------
# DOCUMENTOS NOTARIALES
# ------------------------
class TipoDocumentoEnum(enum.Enum):
    ESCRITURA = "escritura"
    ACTA = "acta"
    TESTIMONIO = "testimonio"

class EstadoDocumentoEnum(enum.Enum):
    BORRADOR = "borrador"
    FIRMADO = "firmado"
    ENTREGADO = "entregado"

class TipoAvisoDocumentoEnum(enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    FISICO = "fisico"

class EstadoEnvioAvisoDocEnum(enum.Enum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    FALLIDO = "fallido"

# ------------------------
# OBLIGACIONES Y EMISIONES
# ------------------------
class TipoObligacionDocumentoGeneralEnum(enum.Enum):
    PAGO_IMPUESTOS = "pago_impuestos"
    PUBLICACION = "publicacion"
    AVISO_TERCEROS = "aviso_terceros"

class TipoEmisionDocumentoAdicionalGeneralEnum(enum.Enum):
    CERTIFICADO = "certificado"
    TESTIMONIO = "testimonio"
    OTRO = "otro"

class EstadoEnvioEmisionGeneralEnum(enum.Enum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    FALLIDO = "fallido"

# ------------------------
# CLAUSULAS Y PUNTOS DE ACTA
# ------------------------
class TipoClausulaEnum(enum.Enum):
    GENERAL = "general"
    OBLIGATORIA = "obligatoria"
    SUGERIDA = "sugerida"
    PERSONALIZADA = "personalizada"

class TipoAplicacionClausulaEnum(enum.Enum):
    DOCUMENTO = "documento"
    ACTA = "acta"
    AMBOS = "ambos"

# ------------------------
# BIENES
# ------------------------
class TipoBienEnum(enum.Enum):
    INMUEBLE = "inmueble"
    MUEBLE = "mueble"
    VEHICULO = "vehiculo"
    OTRO = "otro"

# ------------------------
# TIMBRES Y PROTOCOLOS
# ------------------------
class TipoTimbreGlobalEnum(enum.Enum):
    ESPECIAL = "especial"
    ORDINARIO = "ordinario"
    ELECTRONICO = "electronico"

class MetodoPagoGlobalEnum(enum.Enum):
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    TARJETA = "tarjeta"
    DEBITO = "debito"
    CREDITO = "credito"

# añadido formapago porque se necesita para que funcione la importacion y el migrate
class FormaPagoEnum(enum.Enum):
    """Formas de pago específicas para bufetes (compatibilidad con pagos.py)"""
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    TARJETA = "tarjeta"
    DEBITO = "debito"
    CREDITO = "credito"

class EstadoTimbreGlobalEnum(enum.Enum):
    DISPONIBLE = "disponible"
    UTILIZADO = "utilizado"
    ANULADO = "anulado"

class EstadoPapelProtocoloGlobalEnum(enum.Enum):
    DISPONIBLE = "disponible"
    UTILIZADO = "utilizado"
    ANULADO = "anulado"

# ------------------------
# EXPEDIENTES Y FACTURACION
# ------------------------
class EstadoExpedienteEnum(enum.Enum):
    ABIERTO = "abierto"
    EN_PROCESO = "en_proceso"
    CERRADO = "cerrado"
    ARCHIVADO = "archivado"

class EstadoPagoFacturaEnum(enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    VENCIDO = "vencido"
