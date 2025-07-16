# -*- coding: utf-8 -*-
# archivo: app/models/enums.py
# fecha de creación: 14 / 07 / 25 hora 20:46
# cantidad de lineas originales: 30 aprox.
# ultima actualización: 
# motivo de la actualizacion: 
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90
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

class TipoBienEnum(enum.Enum):
    INMUEBLE = "Inmueble"
    VEHICULO = "Vehículo"
    MUEBLE = "Mueble"
    OTRO = "Otro"
