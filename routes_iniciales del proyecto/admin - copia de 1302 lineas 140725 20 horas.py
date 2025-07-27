# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\admin.py
# Última Actualización: 2025-07-10 21:22:38 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Añadidos prints de depuración para bienes y cláusulas,
#                              Revisión de unicidad para Configuración de Bufete,
#                              Lógica de unicidad para NIT en Persona.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

# Importar solo los modelos que están en core_models.py
from ..models.core_models import db, BufeteJuridico, UsuarioSistema, Notario, Persona, PersonaJuridica, Clausula, Bien, BienInmuebleDetalle, BienMuebleDetalle
# Importar ENUMs necesarios
from ..models.enums import RolUsuarioSistema

# Importar formularios necesarios (solo los que corresponden a los modelos esenciales)
from app.forms import (
    BufeteJuridicoForm, NotarioForm, UsuarioSistemaForm, PersonaForm, PersonaJuridicaForm,
    BienForm, BienInmuebleForm, BienMuebleForm, ClausulaForm
)
# Importar decorador de roles
from app.decorators import role_required

# Importar get_bufete_info desde app.context_processors
from app.context_processors import get_bufete_info

log = logging.getLogger(__name__)

admin_bp = Blueprint('admin_bp', __name__)

# --- Rutas de Gestión de Bufetes ---

@admin_bp.route('/configuracion_bufete', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value)
def configuracion_bufete():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        bufete = _db.session.query(BufeteJuridico).first()
        if not bufete:
            flash('No se encontró información del bufete. Por favor, crea uno.', 'info')
            bufete = BufeteJuridico()

    form = BufeteJuridicoForm(obj=bufete)

    if form.validate_on_submit():
        try:
            # --- Lógica de Validación de Unicidad para el Bufete ---
            # Solo aplicar esta validación si estamos editando un bufete existente
            if bufete.id: # Si el bufete ya existe (estamos editando)
                # Verificar si el nombre_bufete_o_razon_social ya existe en OTRO bufete
                existing_by_name = _db.session.query(BufeteJuridico).filter(
                    BufeteJuridico.nombre_bufete_o_razon_social == form.nombre_bufete_o_razon_social.data,
                    BufeteJuridico.id != bufete.id # Excluir el bufete que estamos editando
                ).first()
                if existing_by_name:
                    flash('Error: El nombre del bufete o razón social ya está registrado para otro bufete.', 'danger')
                    return render_template('admin/configuracion_bufete.html', title='Configuración del Bufete', form=form)

                # Verificar si el colegiado_notario ya existe en OTRO bufete (si el campo no es vacío)
                if form.colegiado_notario.data:
                    existing_by_colegiado = _db.session.query(BufeteJuridico).filter(
                        BufeteJuridico.colegiado_notario == form.colegiado_notario.data,
                        BufeteJuridico.id != bufete.id
                    ).first()
                    if existing_by_colegiado:
                        flash('Error: El número de colegiado del notario ya está registrado para otro bufete.', 'danger')
                        return render_template('admin/configuracion_bufete.html', title='Configuración del Bufete', form=form)

                # Verificar si el nit_notario ya existe en OTRO bufete (si el campo no es vacío y no es 'CF')
                if form.nit_notario.data and form.nit_notario.data.upper() != 'CF':
                    existing_by_nit = _db.session.query(BufeteJuridico).filter(
                        BufeteJuridico.nit_notario == form.nit_notario.data,
                        BufeteJuridico.id != bufete.id
                    ).first()
                    if existing_by_nit:
                        flash('Error: El NIT del notario ya está registrado para otro bufete.', 'danger')
                        return render_template('admin/configuracion_bufete.html', title='Configuración del Bufete', form=form)

            # --- Fin de Lógica de Validación de Unicidad para el Bufete ---

            if not bufete.id:
                # Lógica de creación
                bufete = BufeteJuridico(
                    nombre_bufete_o_razon_social=form.nombre_bufete_o_razon_social.data,
                    nombre_completo_notario=form.nombre_completo_notario.data,
                    colegiado_notario=form.colegiado_notario.data,
                    nit_notario=form.nit_notario.data,
                    direccion_notario=form.direccion_notario.data,
                    telefono_notario=form.telefono_notario.data,
                    email_notario=form.email_notario.data,
                    app_copyright=form.app_copyright.data,
                    nombre_aplicacion=form.nombre_aplicacion.data,
                    maneja_inventario_timbres_papel=form.maneja_inventario_timbres_papel.data,
                    incluye_libreria_plantillas_inicial=form.incluye_libreria_plantillas_inicial.data,
                    habilita_auditoria_borrado_logico=form.habilita_auditoria_borrado_logico.data,
                    habilita_dashboard_avanzado=form.habilita_dashboard_avanzado.data,
                    habilita_ayuda_contextual=form.habilita_ayuda_contextual.data
                )
                _db.session.add(bufete)
                flash('Información del bufete creada exitosamente!', 'success')
            else:
                # Lógica de actualización
                form.populate_obj(bufete)
                flash('Información del bufete actualizada exitosamente!', 'success')

            _db.session.commit()
            return redirect(url_for('admin_bp.configuracion_bufete'))
        except IntegrityError as e:
            _db.session.rollback()
            # Este IntegrityError se capturará si la validación personalizada no lo atrapó,
            # o si hay otra restricción UNIQUE no manejada en la DB para nuevos registros.
            flash(f'Error de integridad: Ya existe un registro con datos duplicados (nombre, colegiado, NIT). ({e.orig})', 'danger')
            log.error(f"IntegrityError al guardar bufete: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al guardar el bufete: {e}', 'danger')
            log.error(f"Error general al guardar bufete: {e}", exc_info=True)
    # RUTA DE PLANTILLA CORREGIDA: 'admin/'
    return render_template('admin/configuracion_bufete.html', title='Configuración del Bufete', form=form)

# --- Rutas de Gestión de Usuarios del Sistema ---
@admin_bp.route('/listado_usuarios_sistema')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_usuarios_sistema():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            usuarios = _db.session.query(UsuarioSistema).filter(
                UsuarioSistema.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value
            ).order_by(UsuarioSistema.nombre_usuario).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            usuarios = _db.session.query(UsuarioSistema).filter(
                UsuarioSistema.bufete_juridico_id == current_user.bufete_juridico_id,
                UsuarioSistema.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value
            ).order_by(UsuarioSistema.nombre_usuario).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver usuarios del sistema.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/listado_usuarios_sistema.html', title='Usuarios del Sistema', usuarios=usuarios)

@admin_bp.route('/agregar_usuario_sistema', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_usuario_sistema():
    form = UsuarioSistemaForm()
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        form.persona_id.choices = [(0, '--- Ninguna ---')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in _db.session.query(Persona).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by('nombres').all()]
        form.notario_id.choices = [(0, '--- Ninguno ---')] + [(n.id, n.nombre_completo) for n in _db.session.query(Notario).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by('nombre_completo').all()]

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif session.get('bufete_activo_id'):
            form.bufete_juridico_id.data = session.get('bufete_activo_id')
            form.bufete_juridico_id.render_kw = {'readonly': True}


    if form.validate_on_submit():
        try:
            nuevo_usuario = UsuarioSistema(
                nombre_usuario=form.nombre_usuario.data,
                nombres=form.nombres.data,
                apellidos=form.apellidos.data,
                email=form.email.data,
                telefono=form.telefono.data,
                direccion_laboral=form.direccion_laboral.data,
                preferencia_contacto_red_social=form.preferencia_contacto_red_social.data,
                rol=form.rol.data,
                is_active=form.is_active.data,
                bufete_juridico_id=form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None,
                persona_id=form.persona_id.data if form.persona_id.data != 0 else None,
                notario_id=form.notario_id.data if form.notario_id.data != 0 else None
            )
            nuevo_usuario.set_password(form.password.data)
            _db.session.add(nuevo_usuario)
            _db.session.commit()
            flash('Usuario del sistema agregado exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error: El nombre de usuario o email ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al agregar usuario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar usuario: {e}', 'danger')
            log.error(f"Error general al agregar usuario: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/agregar_usuario_sistema.html', title='Agregar Nuevo Usuario del Sistema', form=form)

@admin_bp.route('/editar_usuario_sistema/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_usuario_sistema(usuario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        usuario = _db.session.query(UsuarioSistema).get_or_404(usuario_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and usuario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes editar usuarios de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and usuario.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and current_user.id != usuario.id:
            flash('Acceso denegado: No puedes editar a otro Super Administrador.', 'danger')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))

    form = UsuarioSistemaForm(obj=usuario)
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif usuario.bufete_juridico_id:
            form.bufete_juridico_id.data = usuario.bufete_juridico_id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        else:
            form.bufete_juridico_id.data = 0

        form.persona_id.choices = [(0, '--- Ninguna ---')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in _db.session.query(Persona).filter_by(bufete_juridico_id=usuario.bufete_juridico_id).order_by('nombres').all()]
        form.notario_id.choices = [(0, '--- Ninguno ---')] + [(n.id, n.nombre_completo) for n in _db.session.query(Notario).filter_by(bufete_juridico_id=usuario.bufete_juridico_id).order_by('nombre_completo').all()]

        form.persona_id.data = usuario.persona_id if usuario.persona_id else 0
        form.notario_id.data = usuario.notario_id if usuario.notario_id else 0


    if form.validate_on_submit():
        try:
            form.populate_obj(usuario)
            if form.password.data:
                usuario.set_password(form.password.data)

            usuario.persona_id = form.persona_id.data if form.persona_id.data != 0 else None
            usuario.notario_id = form.notario_id.data if form.notario_id.data != 0 else None

            _db.session.commit()
            flash('Usuario del sistema actualizado exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: El nombre de usuario o email ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al editar usuario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al editar usuario: {e}', 'danger')
            log.error(f"Error general al editar usuario: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/editar_usuario_sistema.html', title='Editar Usuario del Sistema', form=form, usuario=usuario)

@admin_bp.route('/eliminar_usuario_sistema/<int:usuario_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_usuario_sistema(usuario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        usuario = _db.session.query(UsuarioSistema).get_or_404(usuario_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and usuario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes eliminar usuarios de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        if usuario.id == current_user.id or usuario.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            flash('Acceso denegado: No puedes eliminar este usuario.', 'danger')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))

        try:
            _db.session.delete(usuario)
            _db.session.commit()
            flash('Usuario del sistema eliminado exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar el usuario porque está asociado a otros registros. ({e.orig})', 'danger')
            log.error(f"IntegrityError al eliminar usuario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar el usuario: {e}', 'danger')
            log.error(f"Error general al eliminar usuario: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_usuarios_sistema'))


# --- Rutas de Gestión de Notarios (Listar) ---
@admin_bp.route('/listado_notarios')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_notarios():
    _db = current_app.extensions['sqlalchemy'] # ACCESO EXPLÍCITO A DB
    with current_app.app_context(): # Asegurar contexto para la consulta
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            notarios = _db.session.query(Notario).order_by(Notario.nombre_completo).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            notarios = _db.session.query(Notario).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by(Notario.nombre_completo).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver notarios.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/listado_notarios.html', title='Notarios Registrados', notarios=notarios)

@admin_bp.route('/agregar_notario', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_notario():
    form = NotarioForm()
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya hay un bufete activo
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif session.get('bufete_activo_id'):
            form.bufete_juridico_id.data = session.get('bufete_activo_id')
            form.bufete_juridico_id.render_kw = {'readonly': True}

    if form.validate_on_submit():
        try:
            nuevo_notario = Notario(
                nombre_completo=form.nombre_completo.data,
                numero_colegiado=form.numero_colegiado.data,
                colegiado_activo=form.colegiado_activo.data,
                fecha_colegiado_activo_verificacion=form.fecha_colegiado_activo_verificacion.data,
                firma_electronica_registrada=form.firma_electronica_registrada.data,
                proveedor_firma_electronica=form.proveedor_firma_electronica.data,
                direccion_laboral=form.direccion_laboral.data,
                telefono=form.telefono.data,
                email=form.email.data,
                preferencia_contacto_red_social=form.preferencia_contacto_red_social.data,
                bufete_juridico_id=form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            )
            _db.session.add(nuevo_notario)
            _db.session.commit()
            flash('Notario agregado exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_notarios'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: El número de colegiado o email ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al agregar notario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar notario: {e}', 'danger')
            log.error(f"Error general al agregar notario: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/agregar_notario.html', title='Agregar Nuevo Notario', form=form)

@admin_bp.route('/editar_notario/<int:notario_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_notario(notario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        notario = _db.session.query(Notario).get_or_404(notario_id)
        # Asegurarse de que el administrador solo edite notarios de su bufete
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and notario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes editar notarios de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_notarios'))

    form = NotarioForm(obj=notario)
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya está asignado
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif notario.bufete_juridico_id:
            form.bufete_juridico_id.data = notario.bufete_juridico_id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        else: # Si no tiene bufete asignado
            form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        try:
            form.populate_obj(notario)
            notario.bufete_juridico_id = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            _db.session.commit()
            flash('Notario actualizado exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_notarios'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: El número de colegiado o email ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al editar notario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al editar notario: {e}', 'danger')
            log.error(f"Error general al editar notario: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'admin/'
    return render_template('admin/editar_notario.html', title='Editar Notario', form=form, notario=notario)

@admin_bp.route('/eliminar_notario/<int:notario_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_notario(notario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        notario = _db.session.query(Notario).get_or_404(notario_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and notario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes eliminar notarios de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_notarios'))

        try:
            _db.session.delete(notario)
            _db.session.commit()
            flash('Notario eliminado exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar el notario porque está asociado a otros registros (ej. documentos). ({e.orig})', 'danger')
            log.error(f"IntegrityError al eliminar notario: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar el notario: {e}', 'danger')
            log.error(f"Error general al eliminar notario: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_notarios'))

# --- Rutas de Gestión de Personas Naturales ---
@admin_bp.route('/listado_personas')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_personas():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            personas = _db.session.query(Persona).order_by(Persona.nombres).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            personas = _db.session.query(Persona).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by(Persona.nombres).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver personas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/listado_clientes.html', title='Personas Naturales', personas=personas)

@admin_bp.route('/agregar_persona', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_persona():
    form = PersonaForm()
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya hay un bufete activo
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif session.get('bufete_activo_id'):
            form.bufete_juridico_id.data = session.get('bufete_activo_id')
            form.bufete_juridico_id.render_kw = {'readonly': True}

        # Poblar choices de testigo_conocimiento_id
        form.testigo_conocimiento_id.choices = [(0, '--- Ninguno ---')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in _db.session.query(Persona).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by('nombres').all()]


    if form.validate_on_submit():
        try:
            # --- LÓGICA DE VALIDACIÓN DE UNICIDAD PARA NIT ---
            if form.nit.data and form.nit.data.upper() != 'CF':
                existing_person = _db.session.query(Persona).filter(
                    Persona.nit == form.nit.data
                ).first()
                if existing_person:
                    flash(f'Error: El NIT "{form.nit.data}" ya está registrado para otra persona.', 'danger')
                    return render_template('clientes/agregar_persona.html', title='Agregar Nueva Persona Natural', form=form)
            # --- FIN DE LÓGICA DE VALIDACIÓN DE UNICIDAD PARA NIT ---
            nueva_persona = Persona(
                nombres=form.nombres.data,
                apellidos=form.apellidos.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                edad_actual_aprox=form.edad_actual_aprox.data,
                estado_civil=form.estado_civil.data,
                nacionalidad=form.nacionalidad.data,
                profesion_oficio=form.profesion_oficio.data,
                domicilio=form.domicilio.data,
                dpi_numero=form.dpi_numero.data,
                nit=form.nit.data,
                dpi_lugar_emision=form.dpi_lugar_emision.data,
                telefono=form.telefono.data,
                email=form.email.data,
                direccion_completa=form.direccion_completa.data,
                identificado_por=form.identificado_por.data,
                testigo_conocimiento_id=form.testigo_conocimiento_id.data if form.testigo_conocimiento_id.data != 0 else None,
                bufete_juridico_id=form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            )
            _db.session.add(nueva_persona)
            _db.session.commit()
            flash('Persona natural agregada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_personas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: El DPI o NIT ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al agregar persona: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar persona: {e}', 'danger')
            log.error(f"Error general al agregar persona: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/agregar_persona.html', title='Agregar Nueva Persona Natural', form=form)

@admin_bp.route('/editar_persona/<int:persona_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_persona(persona_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona = _db.session.query(Persona).get_or_404(persona_id)
        # Asegurarse de que el administrador solo edite personas de su bufete
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes editar personas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_personas'))

    form = PersonaForm(obj=persona)
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya está asignado
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif persona.bufete_juridico_id:
            form.bufete_juridico_id.data = persona.bufete_juridico_id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        else: # Si no tiene bufete asignado
            form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

        # Poblar choices de testigo_conocimiento_id
        form.testigo_conocimiento_id.choices = [(0, '--- Ninguno ---')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in _db.session.query(Persona).filter_by(bufete_juridico_id=persona.bufete_juridico_id).order_by('nombres').all()]
        form.testigo_conocimiento_id.data = persona.testigo_conocimiento_id if persona.testigo_conocimiento_id else 0


    if form.validate_on_submit():
        try:
            # --- LÓGICA DE VALIDACIÓN DE UNICIDAD PARA NIT EN EDICIÓN ---
            # Solo validar si el NIT no es vacío y no es 'CF'
            if form.nit.data and form.nit.data.upper() != 'CF':
                existing_person = _db.session.query(Persona).filter(
                    Persona.nit == form.nit.data,
                    Persona.id != persona_id # Excluir la persona que estamos editando
                ).first()
                if existing_person:
                    flash(f'Error: El NIT "{form.nit.data}" ya está registrado para otra persona.', 'danger')
                    return render_template('clientes/editar_persona.html', title='Editar Persona Natural', form=form, persona=persona)
            # --- FIN DE LÓGICA DE VALIDACIÓN DE UNICIDAD PARA NIT EN EDICIÓN ---

            form.populate_obj(persona)
            persona.testigo_conocimiento_id = form.testigo_conocimiento_id.data if form.testigo_conocimiento_id.data != 0 else None
            persona.bufete_juridico_id = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            _db.session.commit()
            flash('Persona natural actualizada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_personas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: El DPI o NIT ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al editar persona: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al editar persona: {e}', 'danger')
            log.error(f"Error general al editar persona: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/editar_persona.html', title='Editar Persona Natural', form=form, persona=persona)

@admin_bp.route('/eliminar_persona/<int:persona_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_persona(persona_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona = _db.session.query(Persona).get_or_404(persona_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes eliminar personas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_personas'))

        try:
            _db.session.delete(persona)
            _db.session.commit()
            flash('Persona natural eliminada exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar la persona porque está asociada a otros registros (ej. usuarios, documentos). ({e.orig})', 'danger')
            log.error(f"IntegrityError al eliminar persona: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar la persona: {e}', 'danger')
            log.error(f"Error general al eliminar persona: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_personas'))

# --- Rutas de Gestión de Personas Jurídicas ---
@admin_bp.route('/listado_personas_juridicas')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_personas_juridicas():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            personas_juridicas = _db.session.query(PersonaJuridica).order_by(PersonaJuridica.razon_social).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            personas_juridicas = _db.session.query(PersonaJuridica).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by(PersonaJuridica.razon_social).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver personas jurídicas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/listado_clientes.html', title='Personas Jurídicas', personas_juridicas=personas_juridicas)

@admin_bp.route('/agregar_persona_juridica', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_persona_juridica():
    form = PersonaJuridicaForm()
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya hay un bufete activo
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif session.get('bufete_activo_id'):
            form.bufete_juridico_id.data = session.get('bufete_activo_id')
            form.bufete_juridico_id.render_kw = {'readonly': True}

    if form.validate_on_submit():
        try:
            nueva_persona_juridica = PersonaJuridica(
                razon_social=form.razon_social.data,
                nombre_comercial=form.nombre_comercial.data,
                nit=form.nit.data,
                datos_inscripcion_registral=form.datos_inscripcion_registral.data,
                direccion_completa=form.direccion_completa.data,
                telefono=form.telefono.data,
                email=form.email.data,
                bufete_juridico_id=form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            )
            _db.session.add(nueva_persona_juridica)
            _db.session.commit()
            flash('Persona jurídica agregada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_personas_juridicas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: La razón social o NIT ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al agregar persona jurídica: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar persona jurídica: {e}', 'danger')
            log.error(f"Error general al agregar persona jurídica: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/agregar_persona_juridica.html', title='Agregar Nueva Persona Jurídica', form=form)

@admin_bp.route('/editar_persona_juridica/<int:persona_juridica_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_persona_juridica(persona_juridica_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona_juridica = _db.session.query(PersonaJuridica).get_or_404(persona_juridica_id)
        # Asegurarse de que el administrador solo edite personas jurídicas de su bufete
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona_juridica.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes editar personas jurídicas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_personas_juridicas'))

    form = PersonaJuridicaForm(obj=persona_juridica)
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya está asignado
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif persona_juridica.bufete_juridico_id:
            form.bufete_juridico_id.data = persona_juridica.bufete_juridico_id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        else: # Si no tiene bufete asignado
            form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        try:
            form.populate_obj(persona_juridica)
            persona_juridica.bufete_juridico_id = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            _db.session.commit()
            flash('Persona jurídica actualizada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_personas_juridicas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error de integridad: La razón social o NIT ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al editar persona jurídica: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al editar persona jurídica: {e}', 'danger')
            log.error(f"Error general al editar persona jurídica: {e}", exc_info=True)
    # RUTA DE PLANTILLA: 'clientes/'
    return render_template('clientes/editar_persona_juridica.html', title='Editar Persona Jurídica', form=form, persona_juridica=persona_juridica)

@admin_bp.route('/eliminar_persona_juridica/<int:persona_juridica_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_persona_juridica(persona_juridica_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona_juridica = _db.session.query(PersonaJuridica).get_or_404(persona_juridica_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona_juridica.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes eliminar personas jurídicas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_personas_juridicas'))

        try:
            _db.session.delete(persona_juridica)
            _db.session.commit()
            flash('Persona jurídica eliminada exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar la persona jurídica porque está asociada a otros registros. ({e.orig})', 'danger')
            log.error(f"IntegrityError al eliminar persona jurídica: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar la persona jurídica: {e}', 'danger')
            log.error(f"Error general al eliminar persona jurídica: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_personas_juridicas'))

# --- Rutas de Gestión de Cláusulas ---
@admin_bp.route('/listado_clausulas')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.NOTARIO.value)
def listado_clausulas():
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: listado_clausulas - bufete_id_activo: {bufete_id_activo}") # <-- Añadido DEBUG

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para gestionar Cláusulas.', 'warning')
        print("DEBUG: listado_clausulas - Redirigiendo a seleccionar_bufete por bufete_id_activo nulo.") # <-- Añadido DEBUG
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            clausulas = _db.session.query(Clausula).order_by(Clausula.nombre_clausula).all()
        else: # Administrador o Notario
            clausulas = _db.session.query(Clausula).filter_by(bufete_juridico_id=bufete_id_activo).order_by(Clausula.nombre_clausula).all()
        print(f"DEBUG: listado_clausulas - Cantidad de cláusulas encontradas: {len(clausulas)}") # <-- Añadido DEBUG
    # RUTA DE PLANTILLA: 'clausulas/'
    return render_template('clausulas/listado_clausulas.html', title='Biblioteca de Cláusulas', clausulas=clausulas)

@admin_bp.route('/agregar_clausula', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_clausula():
    form = ClausulaForm()
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya hay un bufete activo
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif session.get('bufete_activo_id'):
            form.bufete_juridico_id.data = session.get('bufete_activo_id')
            form.bufete_juridico_id.render_kw = {'readonly': True}

    if form.validate_on_submit():
        try:
            nueva_clausula = Clausula(
                nombre_clausula=form.nombre_clausula.data,
                contenido_base=form.contenido_base.data,
                tipo_clausula=form.tipo_clausula.data,
                tags=form.tags.data,
                editable=form.editable.data,
                fundamentacion_doctrinal_observaciones=form.fundamentacion_doctrinal_observaciones.data,
                fundamentacion_legal_articulos=form.fundamentacion_legal_articulos.data,
                obligatoriedad_sugerencia=form.obligatoriedad_sugerencia.data,
                aplica_a_instrumentos_publicos=form.aplica_a_instrumentos_publicos.data,
                bufete_juridico_id=form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            )
            _db.session.add(nueva_clausula)
            _db.session.commit()
            flash('Cláusula agregada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_clausulas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error: El nombre de cláusula "{form.nombre_clausula.data}" ya existe.', 'danger')
            log.error(f"IntegrityError al agregar cláusula: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar cláusula: {e}', 'danger')
            log.error(f'Ocurrió un error inesperado al agregar cláusula: {e}', exc_info=True)
    # RUTA DE PLANTILLA: 'clausulas/'
    return render_template('clausulas/agregar_clausula.html', title='Agregar Nueva Cláusula', form=form)

@admin_bp.route('/editar_clausula/<int:clausula_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_clausula(clausula_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        clausula = _db.session.query(Clausula).get_or_404(clausula_id)
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and clausula.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes editar cláusulas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_clausulas'))

    form = ClausulaForm(obj=clausula)
    with current_app.app_context():
        # Poblar choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id si es Administrador o si ya está asignado
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
            form.bufete_juridico_id.data = bufetes_disponibles[0].id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        elif clausula.bufete_juridico_id:
            form.bufete_juridico_id.data = clausula.bufete_juridico_id
            form.bufete_juridico_id.render_kw = {'readonly': True}
        else: # Si no tiene bufete asignado
            form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        try:
            # Validar unicidad del nombre de la cláusula (excluyendo la actual)
            existing_clausula = _db.session.query(Clausula).filter(
                Clausula.nombre_clausula == form.nombre_clausula.data,
                Clausula.id != clausula_id,
                Clausula.bufete_juridico_id == (form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None)
            ).first()
            if existing_clausula:
                flash(f'Error: El nombre de cláusula "{form.nombre_clausula.data}" ya existe.', 'danger')
                return render_template('clausulas/editar_clausula.html', form=form, title='Editar Cláusula', clausula=clausula)

            form.populate_obj(clausula)
            clausula.bufete_juridico_id = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            _db.session.commit()
            flash('Cláusula actualizada exitosamente!', 'success')
            return redirect(url_for('admin_bp.listado_clausulas'))
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'Error: El nombre de cláusula "{form.nombre_clausula.data}" ya existe. ({e.orig})', 'danger')
            log.error(f"IntegrityError al editar cláusula: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error inesperado al agregar cláusula: {e}', 'danger')
            log.error(f'Ocurrió un error inesperado al agregar cláusula: {e}', exc_info=True)
    # RUTA DE PLANTILLA: 'clausulas/'
    return render_template('clausulas/editar_clausula.html', form=form, title='Editar Cláusula', clausula=clausula)

@admin_bp.route('/eliminar_clausula/<int:clausula_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_clausula(clausula_id):
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para eliminar cláusulas.', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        clausula = _db.session.query(Clausula).filter_by(id=clausula_id, bufete_juridico_id=bufete_id_activo).first_or_404()
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and clausula.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: No puedes eliminar cláusulas de otros bufetes.', 'danger')
            return redirect(url_for('admin_bp.listado_clausulas'))

        try:
            _db.session.delete(clausula)
            _db.session.commit()
            flash('Cláusula eliminada exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar la cláusula porque está asociada a otros registros (ej. documentos). ({e.orig})', 'danger')
            log.error(f"IntegrityError al eliminar cláusula: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar la cláusula: {e}', 'danger')
            log.error(f"Error general al eliminar cláusula: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_clausulas'))

# --- Rutas de Gestión de Bienes ---
@admin_bp.route('/listado_bienes')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.PROCURADOR.value)
def listado_bienes():
    print("TRACKING: BIENES.PY - Entrando a listado_bienes()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: listado_bienes - bufete_id_activo: {bufete_id_activo}") # <-- Añadido
    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para ver los bienes.', 'warning')
        print("DEBUG: listado_bienes - Redirigiendo a seleccionar_bufete por bufete_id_activo nulo.") # <-- Añadido
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Consultar todos los bienes (inmuebles y muebles) asociados al bufete activo
        bienes = _db.session.query(Bien).filter_by(bufete_juridico_id=bufete_id_activo).order_by(Bien.descripcion_corta).all()
        print(f"DEBUG: listado_bienes - Cantidad de bienes encontrados: {len(bienes)}") # <-- Añadido
    # RUTA DE PLANTILLA: 'bienes/'
    return render_template('bienes/listado_bienes.html', bienes=bienes, title='Gestión de Bienes')

@admin_bp.route('/agregar_inmueble', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_inmueble():
    print("TRACKING: BIENES.PY - Entrando a agregar_inmueble()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: agregar_inmueble - bufete_id_activo: {bufete_id_activo}") # <-- Añadido
    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para agregar bienes inmuebles.', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    form = BienInmuebleForm()

    _db = current_app.extensions['sqlalchemy'] # Acceso a DB para poblar choices
    with current_app.app_context():
        # Lógica para poblar las choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}


    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario agregar_inmueble VALIDADO. Intentando grabar.")
        _db = current_app.extensions['sqlalchemy']
        with current_app.app_context():
            try:
                # Verificar unicidad de Finca, Folio, Libro dentro del mismo bufete
                existing_inmueble = _db.session.query(BienInmuebleDetalle).filter(
                    BienInmuebleDetalle.finca == form.finca.data,
                    BienInmuebleDetalle.folio == form.folio.data,
                    BienInmuebleDetalle.libro == form.libro.data,
                    BienInmuebleDetalle.bufete_juridico_id == bufete_id_activo
                ).first()
                if existing_inmueble:
                    flash(f'Error: Ya existe un inmueble con Finca {form.finca.data}, Folio {form.folio.data}, Libro {form.libro.data} para este bufete.', 'danger')
                    print("TRACKING: BIENES.PY - Error de unicidad detectado.")
                    # RUTA DE PLANTILLA: 'bienes/'
                    return render_template('bienes/agregar_inmueble.html', form=form, title='Agregar Nuevo Bien Inmueble')

                nuevo_inmueble = BienInmuebleDetalle(
                    tipo_bien=form.tipo_bien.data,
                    descripcion_corta=form.descripcion_corta.data,
                    valor_estimado=form.valor_estimado.data,
                    observaciones_bien=form.observaciones_bien.data,
                    bufete_juridico_id=bufete_id_activo,
                    finca=form.finca.data,
                    folio=form.folio.data,
                    libro=form.libro.data,
                    departamento_registro=form.departamento_registro.data,
                    extension_superficial=form.extension_superficial.data,
                    unidad_medida_extension=form.unidad_medida_extension.data,
                    ubicacion_direccion=form.ubicacion_direccion.data,
                    colindancias=form.colindancias.data,
                    numero_registro_fiscal=form.numero_registro_fiscal.data,
                    ultimo_propietario_registral=form.ultimo_propietario_registral.data
                )
                _db.session.add(nuevo_inmueble)
                print(f"TRACKING: BIENES.PY - Objeto nuevo_inmueble añadido a la sesión: {nuevo_inmueble.descripcion_corta}")
                _db.session.commit()
                print(f"DEBUG: agregar_inmueble - Bien inmueble guardado con ID: {nuevo_inmueble.id}, Bufete ID: {nuevo_inmueble.bufete_juridico_id}") # <-- Añadido
                print("TRACKING: BIENES.PY - COMMIT de nuevo_inmueble realizado exitosamente.")
                flash('Bien Inmueble agregado exitosamente!', 'success')
                return redirect(url_for('admin_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar inmueble. Verifique datos únicos (ej. Finca/Folio/Libro, Registro Fiscal). ({e.orig})', 'danger')
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit: {e.orig}")
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al agregar inmueble: {e}', 'danger')
                log.error(f"Error general al agregar inmueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario agregar_inmueble NO VALIDADO.")
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}")
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}")
    # RUTA DE PLANTILLA: 'bienes/'
    return render_template('bienes/agregar_inmueble.html', form=form, title='Agregar Nuevo Bien Inmueble')

@admin_bp.route('/editar_inmueble/<int:bien_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_inmueble(bien_id):
    print("TRACKING: BIENES.PY - Entrando a editar_inmueble()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: editar_inmueble - bufete_id_activo: {bufete_id_activo}") # <-- Añadido
    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para editar bienes. (Error: No hay bufete activo en sesión)', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        inmueble = _db.session.query(BienInmuebleDetalle).filter_by(id=bien_id, bufete_juridico_id=bufete_id_activo).first_or_404()

    form = BienInmuebleForm(obj=inmueble)

    _db = current_app.extensions['sqlalchemy'] # Acceso a DB para poblar choices
    with current_app.app_context():
        # Lógica para poblar las choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}
            else: # Si no tiene bufete asignado
                 form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario editar_inmueble VALIDADO. Intentando grabar.")
        _db = current_app.extensions['sqlalchemy']
        with current_app.app_context():
            try:
                # Validación de unicidad para OTROS bienes en el mismo bufete
                existing_inmueble = _db.session.query(BienInmuebleDetalle).filter(
                    BienInmuebleDetalle.finca == form.finca.data,
                    BienInmuebleDetalle.folio == form.folio.data,
                    BienInmuebleDetalle.libro == form.libro.data,
                    BienInmuebleDetalle.bufete_juridico_id == bufete_id_activo,
                    BienInmuebleDetalle.id != bien_id
                ).first()
                if existing_inmueble:
                    flash(f'Error: Ya existe otro inmueble con Finca {form.finca.data}, Folio {form.folio.data}, Libro {form.libro.data} para este bufete.', 'danger')
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en edición.")
                    # RUTA DE PLANTILLA: 'bienes/'
                    return render_template('bienes/editar_inmueble.html', form=form, title='Editar Bien Inmueble', bien=inmueble)

                inmueble.descripcion_corta = form.descripcion_corta.data
                inmueble.valor_estimado = form.valor_estimado.data
                inmueble.observaciones_bien = form.observaciones_bien.data
                inmueble.finca = form.finca.data
                inmueble.folio = form.folio.data
                inmueble.libro = form.libro.data
                inmueble.departamento_registro = form.departamento_registro.data
                inmueble.extension_superficial = form.extension_superficial.data
                inmueble.unidad_medida_extension = form.unidad_medida_extension.data
                inmueble.ubicacion_direccion = form.ubicacion_direccion.data # Asegúrate de que estos campos se actualicen
                inmueble.colindancias = form.colindancias.data
                inmueble.numero_registro_fiscal = form.numero_registro_fiscal.data
                inmueble.ultimo_propietario_registral = form.ultimo_propietario_registral.data

                _db.session.commit()
                print("TRACKING: BIENES.PY - COMMIT de inmueble editado realizado exitosamente.")
                flash('Bien Inmueble actualizado exitosamente!', 'success')
                return redirect(url_for('admin_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar inmueble. Verifique datos únicos (ej. Finca/Folio/Libro, Registro Fiscal). ({e.orig})', 'danger')
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de edición: {e.orig}")
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al editar inmueble: {e}', 'danger')
                log.error(f"Error general al editar inmueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario editar_inmueble NO VALIDADO.")
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}")
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}")
    # RUTA DE PLANTILLA: 'bienes/'
    return render_template('bienes/editar_inmueble.html', form=form, title='Editar Bien Inmueble', bien=inmueble)

@admin_bp.route('/agregar_mueble', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_mueble():
    print("TRACKING: BIENES.PY - Entrando a agregar_mueble()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: agregar_mueble - bufete_id_activo: {bufete_id_activo}") # <-- Añadido
    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para agregar bienes muebles.', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    form = BienMuebleForm()

    _db = current_app.extensions['sqlalchemy'] # Acceso a DB para poblar choices
    with current_app.app_context():
        # Lógica para poblar las choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}
            else: # Si no tiene bufete asignado
                 form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario agregar_mueble VALIDADO. Intentando grabar.")
        _db = current_app.extensions['sqlalchemy']
        with current_app.app_context():
            try:
                # Validación de unicidad
                existing_mueble = _db.session.query(BienMuebleDetalle).filter(
                    (BienMuebleDetalle.numero_placa == form.numero_placa.data) | \
                    (BienMuebleDetalle.numero_identificacion_vehicular_vin == form.numero_identificacion_vehicular_vin.data),
                    BienMuebleDetalle.bufete_juridico_id == bufete_id_activo
                ).first()
                if existing_mueble:
                    flash(f'Error: Ya existe un mueble con la misma placa o VIN para este bufete.', 'danger')
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en agregar mueble.")
                    # RUTA DE PLANTILLA: 'bienes/'
                    return render_template('bienes/agregar_mueble.html', form=form, title='Agregar Nuevo Bien Mueble')

                nuevo_mueble = BienMuebleDetalle(
                    tipo_bien=form.tipo_bien.data,
                    descripcion_corta=form.descripcion_corta.data,
                    valor_estimado=form.valor_estimado.data,
                    observaciones_bien=form.observaciones_bien.data,
                    bufete_juridico_id=bufete_id_activo,
                    marca=form.marca.data,
                    modelo=form.modelo.data,
                    tipo_vehiculo=form.tipo_vehiculo.data,
                    numero_motor=form.numero_motor.data,
                    numero_chasis=form.numero_chasis.data,
                    numero_placa=form.numero_placa.data,
                    color=form.color.data,
                    numero_identificacion_vehicular_vin=form.numero_identificacion_vehicular_vin.data
                )
                _db.session.add(nuevo_mueble)
                print(f"TRACKING: BIENES.PY - Objeto nuevo_mueble añadido a la sesión: {nuevo_mueble.descripcion_corta}")
                _db.session.commit()
                print(f"DEBUG: agregar_mueble - Bien mueble guardado con ID: {nuevo_mueble.id}, Bufete ID: {nuevo_mueble.bufete_juridico_id}") # <-- Añadido
                print("TRACKING: BIENES.PY - COMMIT de nuevo_mueble realizado exitosamente.")
                flash('Bien Mueble agregado exitosamente!', 'success')
                return redirect(url_for('admin_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar mueble. Verifique datos únicos (ej. Número de Placa, VIN). ({e.orig})', 'danger')
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de agregar mueble: {e.orig}")
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al agregar mueble: {e}', 'danger')
                log.error(f"Error general al agregar mueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario agregar_mueble NO VALIDADO.")
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}")
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}")
    # RUTA DE PLANTILLA: 'bienes/' - ELIMINADO 'bien=mueble' de aquí ya que no existe al agregar
    return render_template('bienes/agregar_mueble.html', form=form, title='Agregar Nuevo Bien Mueble')

@admin_bp.route('/editar_mueble/<int:bien_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_mueble(bien_id):
    print("TRACKING: BIENES.PY - Entrando a editar_mueble()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None
    print(f"DEBUG: editar_mueble - bufete_id_activo: {bufete_id_activo}") # <-- Añadido
    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para editar bienes. (Error: No hay bufete activo en sesión)', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        mueble = _db.session.query(BienMuebleDetalle).filter_by(id=bien_id, bufete_juridico_id=bufete_id_activo).first_or_404()

    form = BienMuebleForm(obj=mueble)

    _db = current_app.extensions['sqlalchemy'] # Acceso a DB para poblar choices
    with current_app.app_context():
        # Lógica para poblar las choices del campo bufete_juridico_id
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        else: # Super Administrador
            bufetes_disponibles = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()

        form.bufete_juridico_id.choices = [(0, '--- Seleccionar Bufete ---')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}
            else: # Si no tiene bufete asignado
                 form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario editar_mueble VALIDADO. Intentando grabar.")
        _db = current_app.extensions['sqlalchemy']
        with current_app.app_context():
            try:
                # Validación de unicidad para otros bienes (excluyendo el que se está editando)
                existing_mueble = _db.session.query(BienMuebleDetalle).filter(
                    (BienMuebleDetalle.numero_placa == form.numero_placa.data) | \
                    (BienMuebleDetalle.numero_identificacion_vehicular_vin == form.numero_identificacion_vehicular_vin.data),
                    BienMuebleDetalle.bufete_juridico_id == bufete_id_activo,
                    BienMuebleDetalle.id != bien_id
                ).first()
                if existing_mueble:
                    flash(f'Error: Ya existe otro mueble con la misma placa o VIN para este bufete.', 'danger')
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en edición de mueble.")
                    # RUTA DE PLANTILLA: 'bienes/'
                    return render_template('bienes/editar_mueble.html', form=form, title='Editar Bien Mueble', bien=mueble)

                mueble.descripcion_corta = form.descripcion_corta.data
                mueble.valor_estimado = form.valor_estimado.data
                mueble.observaciones_bien = form.observaciones_bien.data
                mueble.marca = form.marca.data
                mueble.modelo = form.modelo.data
                mueble.tipo_vehiculo = form.tipo_vehiculo.data
                mueble.numero_motor = form.numero_motor.data
                mueble.numero_chasis = form.numero_chasis.data
                mueble.numero_placa = form.numero_placa.data
                mueble.color = form.color.data
                mueble.numero_identificacion_vehicular_vin = form.numero_identificacion_vehicular_vin.data

                _db.session.commit()
                print("TRACKING: BIENES.PY - COMMIT de mueble editado realizado exitosamente.")
                flash('Bien Mueble actualizado exitosamente!', 'success')
                return redirect(url_for('admin_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar mueble. Verifique datos únicos (ej. Número de Placa, VIN). ({e.orig})', 'danger')
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de edición de mueble: {e.orig}")
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al editar mueble: {e}', 'danger')
                log.error(f"Error general al editar mueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario editar_mueble NO VALIDADO.")
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}")
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}")
    # RUTA DE PLANTILLA: 'bienes/'
    return render_template('bienes/editar_mueble.html', form=form, title='Editar Bien Mueble', bien=mueble)

@admin_bp.route('/eliminar_bien/<int:bien_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_bien(bien_id):
    print("TRACKING: BIENES.PY - Entrando a eliminar_bien()")
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para eliminar bienes.', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        bien = _db.session.query(Bien).filter_by(id=bien_id, bufete_juridico_id=bufete_id_activo).first_or_404()
        try:
            _db.session.delete(bien)
            print(f"TRACKING: BIENES.PY - Objeto bien eliminado de la sesión: {bien.descripcion_corta}")
            _db.session.commit()
            print("TRACKING: BIENES.PY - COMMIT de eliminación de bien realizado exitosamente.")
            flash('Bien eliminado exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            flash(f'No se puede eliminar el bien porque está asociado a otros registros (ej. documentos). ({e.orig})', 'danger')
            print(f"TRACKING: BIENES.PY - IntegrityError durante commit de eliminación: {e.orig}")
        except Exception as e:
            _db.session.rollback()
            flash(f'Ocurrió un error al eliminar el bien: {e}', 'danger')
            print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit de eliminación: {e}")
            log.error(f"Error general al eliminar bien: {e}", exc_info=True)
    return redirect(url_for('admin_bp.listado_bienes'))