# archivo: scripts/seed_inicial.py
# fecha de creación: 29 / 07 / 25
# última actualización: 29 / 07 / 25 hora 13:40
# motivo: corregir inserción usando .value de enums para PostgreSQL
# autor: Giancarlo F. + Tars-90

from app import create_app, db
from app.models.usuarios import Usuario
from app.models.enums import RolUsuarioEnum, EstadoUsuarioEnum, TipoClausulaEnum, TipoAplicacionClausulaEnum
from app.models.clausulas_puntos import ClausulasPuntos

app = create_app()

with app.app_context():
    print("🌱 Iniciando seed inicial...")

    # Usuarios base
    if not Usuario.query.filter_by(username="admin").first():
        db.session.add(Usuario(
            username="admin",
            correo="admin@bufete.com",
            password_hash="admin123",
            rol=RolUsuarioEnum.SUPERADMIN.value,
            estado=EstadoUsuarioEnum.ACTIVO.value,
            bufete_id=1
        ))

    if not Usuario.query.filter_by(username="notario_demo").first():
        db.session.add(Usuario(
            username="notario_demo",
            correo="notario@bufete.com",
            password_hash="notario123",
            rol=RolUsuarioEnum.NOTARIO.value,
            estado=EstadoUsuarioEnum.ACTIVO.value,
            bufete_id=1
        ))

    if not Usuario.query.filter_by(username="admin_local").first():
        db.session.add(Usuario(
            username="admin_local",
            correo="local@bufete.com",
            password_hash="local123",
            rol=RolUsuarioEnum.ADMIN_LOCAL.value,
            estado=EstadoUsuarioEnum.ACTIVO.value,
            bufete_id=1
        ))

    # Clausulas iniciales
    clausulas_iniciales = [
        "CLÁUSULA ESPECIAL", "CLÁUSULA ADICIONAL", "CLÁUSULA FINANCIERA",
        "CLÁUSULA OPERATIVA", "CLÁUSULA ADMINISTRATIVA", "GENERAL",
        "ESPECÍFICA", "DEFINICIONES", "CONFIDENCIALIDAD",
        "RESOLUCIÓN DE CONTROVERSIAS", "CAUSAS DE RESARCIMIENTO",
        "RESCISIÓN", "TERMINACIÓN ANTICIPADA",
        "FUERZA MAYOR Y CASO FORTUITO", "CESIÓN DE DERECHOS",
        "SUBCONTRATACIÓN", "PENALIZACIONES", "ACUERDOS PREVIOS",
        "PRECIO Y FORMA DE PAGO", "ENTREGA Y RECEPCIÓN", "SANEAMIENTO",
        "EVICCIÓN Y VICIOS OCULTOS", "GASTOS E IMPUESTOS"
    ]

    for c in clausulas_iniciales:
        if not ClausulasPuntos.query.filter_by(nombre=c).first():
            db.session.add(
                ClausulasPuntos(
                    nombre=c.upper(),
                    contenido=f"Contenido base de {c.title()}...",
                    tipo=TipoClausulaEnum.GENERAL,
                    aplicacion=TipoAplicacionClausulaEnum.AMBOS
                )
            )

    db.session.commit()
    print("✅ Seed inicial completado correctamente.")
