# -*- coding: utf-8 -*-
# archivo: app/models/enums.py
# fecha de creación: 14 / 07 / 25 hora 20:46
# cantidad de lineas originales: 30 aprox.
# ultima actualización: 
# motivo de la actualizacion: 
# lineas actuales: ____
# autor: Giancarlo F. + Tars-90

"""
Enumeraciones de tipos de documento, estado, usuario y más.
"""

import enum

class TipoDocumentoEnum(enum.Enum):
    ESCRITURA_PUBLICA = "Escritura Pública"
    ACTA_NOTARIAL = "Acta Notarial"
    AVISO = "Aviso"
    CIERRE_PROTOCOLO = 'Cierre Protocolo'
    INDICE_ANUAL = 'Índice Anual'
class EstadoDocumentoGeneralEnum(enum.Enum):
    BORRADOR = 'Borrador'
    EN_PROCESO = 'En Proceso'
    FINALIZADO = 'Finalizado'
    ANULADO = 'Anulado'
    
class EstadoDocumentoEnum(enum.Enum):
    BORRADOR = "Borrador"
    EN_REVISION = "En Revisión"
    FINALIZADO = "Finalizado"
    ENTREGADO = "Entregado"
    ANULADO = "Anulado"
    ABIERTO = 'Abierto'
    CERRADO = 'Cerrado'
    ARCHIVADO = 'Archivado'
    PENDIENTE = 'Pendiente'

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

class TipoBienEnum(enum.Enum):
    INMUEBLE = "Inmueble"
    VEHICULO = "Vehículo"
    MUEBLE = "Mueble"
    OTRO = "Otro"

class TipoClausulaEnum(enum.Enum):
    GENERAL = 'General'
    ESPECIFICA = 'Específica'
    DEFINICIONES = 'Definiciones'
    OBLIGACIONES = 'Obligaciones'
    DERECHOS = 'Derechos'
    GARANTIAS = 'Garantías'
    REPRESENTACIONES_GARANTIAS = 'Representaciones y Garantías'
    CONDICIONES = 'Condiciones'
    DISPOSICIONES_FINALES = 'Disposiciones Finales'
    LEGISLACION_APLICABLE = 'Legislación Aplicable'
    JURISDICCION_COMPETENCIA = 'Jurisdicción y Competencia'
    NOTIFICACIONES = 'Notificaciones'
    CONFIDENCIALIDAD = 'Confidencialidad'
    RESOLUCION_CONTROVERSIAS = 'Resolución de Controversias'
    CAUSAS_RESARCIMIENTO = 'Causas de Resarcimiento'
    RESCISION = 'Rescisión'
    TERMINACION_ANTICIPADA = 'Terminación Anticipada'
    FUERZA_MAYOR_CASO_FORTUITO = 'Fuerza Mayor y Caso Fortuito'
    CESION_DE_DERECHOS = 'Cesión de Derechos'
    SUBCONTRATACION = 'Subcontratación'
    PENALIZACIONES = 'Penalizaciones'
    ACUERDOS_PREVIOS = 'Acuerdos Previos'
    ENCABEZADOS_TITULOS = 'Encabezados y Títulos'
    DIVISION_DE_CLAUSULAS = 'División de Cláusulas'
    COMPARECENCIA = 'Comparecencia'
    ESTIPULACIONES_BASICAS = 'Estipulaciones Básicas'
    IDENTIFICACION_PARTES = 'Identificación de Partes'
    NATURALEZA_CONTRATO = 'Naturaleza del Contrato'
    PRECIO_FORMA_PAGO = 'Precio y Forma de Pago'
    ENTREGA_RECEPCION = 'Entrega y Recepción'
    SANEAMIENTO = 'Saneamiento'
    EVICCION_VVICIOS_OCULTOS = 'Evicción y Vicios Ocultos'
    GASTOS_IMPUESTOS = 'Gastos e Impuestos'
    REGISTRO_PUBLICO = 'Registro Público'
    PROTOCOLIZACION = 'Protocolización'
    TESTIMONIOS = 'Testimonios'
    DISPOSICIONES_NOTARIALES = 'Disposiciones Notariales'
    ACEPTACION = 'Aceptación'
    LECTURA_FIRMA = 'Lectura y Firma'
    LEGALIZACION_FIRMAS = 'Legalización de Firmas'
    AUTENTICACION_COPIAS = 'Autenticación de Copias'
    DECLARACIONES_JURADAS = 'Declaraciones Juradas'
    PODERES = 'Poderes'
    MANDATOS = 'Mandatos'
    REVOCACION = 'Revocación'
    SUSTITUCION = 'Sustitución'
    RENOVACION = 'Renovación'
    MODIFICACION = 'Modificación'
    ADENDUM = 'Adendum'
    REPRESENTACION_COMPAÑIA = 'Representación de Compañía'
    CAPACIDAD_LEGAL = 'Capacidad Legal'
    OBJETO_ILICITO = 'Objeto Ilícito'
    CAUSA_ILICITA = 'Causa Ilícita'
    VICIOS_CONSENTIMIENTO = 'Vicios del Consentimiento'
    INTERPRETACION = 'Interpretación'
    INTEGRALIDAD = 'Integralidad'
    SEPARABILIDAD = 'Separabilidad'
    NO_RENUNCIA = 'No Renuncia'
    LEY_APLICABLE = 'Ley Aplicable'
    RESOLUCION_CONFLICTOS = 'Resolución de Conflictos'
    ARBITRAJE = 'Arbitraje'
    COMPROMISO = 'Compromiso'
    TRANSACCION = 'Transacción'
    PRESCRIPCION = 'Prescripción'
    CADUCIDAD = 'Caducidad'
    FUERZA_EJECUTIVA = 'Fuerza Ejecutiva'
    INSCRIPCION_REGISTRAL = 'Inscripción Registral'
    AVISOS_REGISTRALES = 'Avisos Registrales'
    IMPUESTO_VALOR_AGREGADO = 'Impuesto al Valor Agregado'
    IMPUESTO_TIMBRE_FISCAL = 'Impuesto de Timbre Fiscal'
    IMPUESTO_TIMBRE_NOTARIAL = 'Impuesto de Timbre Notarial'
    IMPUESTOS_MUNICIPALES = 'Impuestos Municipales'
    EXENCIONES = 'Exenciones'
    CERTIFICACIONES = 'Certificaciones'
    ANOTACIONES = 'Anotaciones'
    CANCELACIONES = 'Cancelaciones'
    PROTOCOLOS_NOTARIALES = 'Protocolos Notariales'
    ACTAS_PROTOCOLIZACION = 'Actas de Protocolización'
    REQUERIMIENTOS = 'Requerimientos'
    NOMBRAMIENTOS = 'Nombramientos'
    REVOCACION_PODERES = 'Revocación de Poderes'
    SUSTITUCION_PODERES = 'Sustitución de Poderes'
    RECONOCIMIENTO_DEUDA = 'Reconocimiento de Deuda'
    PROMESA_VENTA = 'Promesa de Venta'
    OPCION_COMPRA = 'Opción de Compra'
    DEPOSITO = 'Depósito'
    PRENDA = 'Prenda'
    HIPOTECA = 'Hipoteca'
    FIANZA = 'Fianza'
    SOLIDARIDAD = 'Solidaridad'
    SUBSIDIARIEDAD = 'Subsidiariedad'
    CLAUSULA_ESPECIAL = 'Cláusula Especial'
    CLAUSULA_ADICIONAL = 'Cláusula Adicional'
    CLAUSULA_FINANCIERA = 'Cláusula Financiera'
    CLAUSULA_OPERATIVA = 'Cláusula Operativa'
    CLAUSULA_ADMINISTRATIVA = 'Cláusula Administrativa'

class RolEnDocumentoParteEnum(enum.Enum):
    OTORGANTE = 'Otorgante'
    RECEPTOR = 'Receptor'
    TESTIGO = 'Testigo'
    COMPRADOR = 'Comprador'
    VENDEDOR = 'Vendedor'
    MUTUANTE = 'Mutuante'
    MUTUARIO = 'Mutuario'
    DEUDOR = 'Deudor'
    ACREEDOR = 'Acreedor'
    APODERADO = 'Apoderado'
    REPRESENTANTE_LEGAL = 'Representante Legal'
    ARRENDADOR = 'Arrendador' 
    ARRENDATARIO = 'Arrendatario' 
    PROMITENTE_VENDEDOR = 'Promitente Vendedor'
    PROMITENTE_COMPRADOR = 'Promitente Comprador'
    CONTRATISTA = 'Contratista'
    CONTRATANTE = 'Contratante'
    ADMINISTRADOR_INMUEBLE = 'Administrador de Inmueble'
    FIDEICOMITENTE = 'Fideicomitente'
    FIDEICOMISARIO = 'Fideicomisario'
    FIDUCIARIO = 'Fiduciario'
    DONANTE = 'Donante' 
    DONATARIO = 'Donatario' 
    CEDENTE = 'Cedente'
    CESIONARIO = 'Cesionario'
    SOCIO = 'Socio'
    PRESIDENTE = 'Presidente'
    SECRETARIO = 'Secretario'
    TESORERO = 'Tesorero'
    DIRECTOR = 'Director'
    GERENTE = 'Gerente'
    MIEMBRO = 'Miembro'
    AUDITOR = 'Auditor'
    LIQUIDADOR = 'Liquidador'
    CURADOR = 'Curador'
    TUTOR = 'Tutor'
    ALBACEA = 'Albaceas'
    HEREDERO = 'Heredero'
    LEGATARIO = 'Legatario'
    BENEFICIARIO = 'Beneficiario'
    GARANTE = 'Garante' 
    OTROS = 'Otros'

class TipoObligacionDocumentoGeneralEnum(enum.Enum):
    PREVIA = 'Previa'
    POSTERIOR = 'Posterior'
    AVISO = 'Aviso'
    TIMBRE = 'Timbre'
    RECORDATORIO = 'Recordatorio'
    OPCIONAL = 'Opcional'
    SUGERIDA = 'Sugerida'
    OBLIGATORIA = 'Obligatoria'
    
class EstadoEnvioEmisionGeneralEnum(enum.Enum):
    CREADO = 'Creado'
    ENVIADO = 'Enviado'
    RECIBIDO = 'Recibido'
    RECHAZADO = 'Rechazado'
    CUMPLIDO = 'Cumplido'
    PENDIENTE_ENVIO = 'Pendiente de Envio'
    

    
class MetodoPagoGlobalEnum(enum.Enum):
    EFECTIVO = 'Efectivo'
    TARJETA = 'Tarjeta'
    CHEQUE = 'Cheque'
    TRANSFERENCIA = 'Transferencia'
    OTRO = 'Otro'

class EstadoTimbreGlobalEnum(enum.Enum):
    ACTIVO = 'Activo'
    AGOTADO = 'Agotado'

class EstadoPapelProtocoloGlobalEnum(enum.Enum):
    ACTIVO = 'Activo'
    AGOTADO = 'Agotado'

class TipoEmisionDocumentoAdicionalGeneralEnum(enum.Enum):
    PRIMER_TESTIMONIO = 'Primer Testimonio'
    SEGUNDO_TESTIMONIO = 'Segundo Testimonio'
    COPIA_SIMPLE = 'Copia Simple'
    COPIA_LEGALIZADA = 'Copia Legalizada'
    ESPECIAL = 'Especial'

class TipoAvisoDocumentoEnum(enum.Enum):
    CANCELACION = 'Cancelación'
    TRASPASO = 'Traspaso'
    VENTA = 'Venta'
    MATRIMONIO = 'Matrimonio'
    RECTIFICACION = 'Rectificación'
    TESTIMONIO_ESPECIAL = 'Testimonio Especial'
    TRIMESTRAL = 'Trimestral'
    CIERRE_PROTOCOLO = 'Cierre Protocolo'
    INDICE_ANUAL = 'Índice Anual'
    OTROS = 'Otros'
    
class AnversoReversoEnum(enum.Enum):
    ANVERSO = 'a'
    REVERSO = 'v'
    
class EstadoPagoFacturaEnum(enum.Enum): # pagos de los planes
    PENDIENTE = 'Pendiente'
    PAGADA = 'Pagada'
    ANULADA = 'Anulada'
    
class TipoTimbreGlobalEnum(PyEnum):
    FISCAL = 'Fiscal'
    NOTARIAL = 'Notarial'
class TipoTimbreSugeridoObligacionEnum(PyEnum): # sugerira para los documentos que timbre utilizar
    FISCAL = 'Fiscal'
    NOTARIAL = 'Notarial'