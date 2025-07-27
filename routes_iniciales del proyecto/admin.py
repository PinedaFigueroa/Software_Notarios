# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\admin.py
# Última Actualización: 2025-07-18 21:15:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Sincronización de importaciones con modelos actualizados.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime 

# Importar modelos
from app.models.core_models import db, BufeteJuridico, UsuarioSistema, Notario, Persona, PersonaJuridica, \
                                   DocumentoNotarial, PlantillaDocumentoNotarial, Expediente, Factura, Bien, Clausula # Mantener la importación de todos los modelos que se usan o puedan usar
# Importar ENUMs necesarios
from app.models.enums import RolUsuarioSistema

# Importar formularios necesarios
from app.forms import BufeteJuridicoForm, NotarioForm, UsuarioSistemaForm, PersonaForm, PersonaJuridicaForm, \
                      PlantillaDocumentoNotarialForm, ExpedienteForm, FacturaForm, BienForm, ClausulaForm

# Importar decorador de roles
from app.decorators import role_required

log = logging.getLogger(__name__)

admin_bp = Blueprint('admin_bp', __name__)

# --- Rutas de Gestión de Bufetes ---

@admin_bp.route('/configuracion_bufete', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def configuracion_bufete():
    _db = current_app.extensions['sqlalchemy']
    
    bufete_id_activo = None
    if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
        if not current_user.bufete_juridico_id:
            flash('Tu cuenta de administrador no está asociada a ningún bufete. Contacta al Super Administrador.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
        bufete_id_activo = current_user.bufete_juridico_id
    elif current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
        bufete_id_activo = session.get('bufete_activo_id') 
        if not bufete_id_activo:
            flash('Por favor, selecciona un bufete para acceder a su configuración.', 'warning')
            return redirect(url_for('main_bp.seleccionar_bufete'))
    else:
        flash('Acceso denegado: No tienes permisos para acceder a esta sección.', 'danger')
        return redirect(url_for('main_bp.dashboard'))

    with current_app.app_context():
        bufete = _db.session.query(BufeteJuridico).get_or_404(bufete_id_activo)

        form = BufeteJuridicoForm(obj=bufete)

        if form.validate_on_submit():
            form.populate_obj(bufete)

            if not form.nombre_aplicacion.data:
                bufete.nombre_aplicacion = "Sistema Notarial Hubsa"
            if not form.app_copyright.data:
                bufete.app_copyright = f"© {datetime.now().year} Sistema Notarial Hubsa / Todos los derechos reservados."

            try:
                _db.session.commit()
                flash('Configuración del bufete actualizada exitosamente.', 'success')
                return redirect(url_for('admin_bp.configuracion_bufete'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar bufete: {e.orig}', 'danger')
                log.error(f"IntegrityError al actualizar configuración de bufete: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar la configuración del bufete: {e}', 'danger')
                log.error(f"Error al actualizar configuración de bufete: {e}", exc_info=True)

    return render_template('admin/configuracion_bufete.html', title='Configuración del Bufete', form=form, bufete=bufete)


@admin_bp.route('/listado_bufetes')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value) 
def listado_bufetes():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        bufetes = _db.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
    
    return render_template('admin/listado_bufetes.html', title='Gestión de Bufetes', bufetes=bufetes)


@admin_bp.route('/agregar_bufete', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value)
def agregar_bufete():
    _db = current_app.extensions['sqlalchemy']
    form = BufeteJuridicoForm()

    if form.validate_on_submit():
        with current_app.app_context():
            nombre_aplicacion_final = form.nombre_aplicacion.data if form.nombre_aplicacion.data else "Sistema Notarial Hubsa"
            app_copyright_final = form.app_copyright.data if form.app_copyright.data else f"© {datetime.now().year} Sistema Notarial Hubsa / Todos los derechos reservados."

            nuevo_bufete = BufeteJuridico(
                nombre_bufete_o_razon_social=form.nombre_bufete_o_razon_social.data,
                nombre_completo_notario=form.nombre_completo_notario.data,
                colegiado_notario=form.colegiado_notario.data,
                nit_notario=form.nit_notario.data,
                direccion_notario=form.direccion_notario.data,
                telefono_notario=form.telefono_notario.data,
                email_notario=form.email_notario.data,
                app_copyright=app_copyright_final,
                nombre_aplicacion=nombre_aplicacion_final,
                maneja_inventario_timbres_papel=form.maneja_inventario_timbres_papel.data,
                incluye_libreria_plantillas_inicial=form.incluye_libreria_plantillas_inicial.data,
                habilita_auditoria_borrado_logico=form.habilita_auditoria_borrado_logico.data,
                habilita_dashboard_avanzado=form.habilita_dashboard_avanzado.data,
                habilita_ayuda_contextual=form.habilita_ayuda_contextual.data,
                is_active=form.is_active.data 
            )
            
            _db.session.add(nuevo_bufete)
            try:
                _db.session.commit()
                flash('Nuevo bufete agregado exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_bufetes'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar bufete: {e.orig}. Asegúrate de que el nombre del bufete sea único.', 'danger')
                log.error(f"IntegrityError al agregar bufete: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al agregar el bufete: {e}', 'danger')
                log.error(f"Error general al agregar bufete: {e}", exc_info=True)

    return render_template('admin/agregar_bufete.html', title='Agregar Nuevo Bufete', form=form)


@admin_bp.route('/editar_bufete/<int:bufete_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value) 
def editar_bufete(bufete_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        bufete = _db.session.query(BufeteJuridico).get_or_404(bufete_id)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            flash('Acceso denegado: Los administradores solo pueden configurar su propio bufete desde la opción "Configuración del Bufete".', 'danger')
            return redirect(url_for('admin_bp.configuracion_bufete'))

        form = BufeteJuridicoForm(obj=bufete)

        if form.validate_on_submit():
            form.populate_obj(bufete)

            if not form.nombre_aplicacion.data:
                bufete.nombre_aplicacion = "Sistema Notarial Hubsa"
            if not form.app_copyright.data:
                bufete.app_copyright = f"© {datetime.now().year} Sistema Notarial Hubsa / Todos los derechos reservados."

            try:
                _db.session.commit()
                flash('Configuración del bufete actualizada exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_bufetes')) 
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar bufete: {e.orig}. Asegúrate de que el nombre del bufete sea único.', 'danger')
                log.error(f"IntegrityError al actualizar configuración de bufete: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar la configuración del bufete: {e}', 'danger')
                log.error(f"Error general al actualizar bufete: {e}", exc_info=True)

    return render_template('admin/editar_bufete.html', title='Editar Bufete', form=form, bufete=bufete)


@admin_bp.route('/eliminar_bufete/<int:bufete_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value)
def eliminar_bufete(bufete_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        bufete = _db.session.query(BufeteJuridico).get_or_404(bufete_id)

        if _db.session.query(BufeteJuridico).filter_by(is_active=True).count() == 1 and bufete.is_active:
             flash('No se puede inhabilitar el único bufete activo en el sistema. Debe haber al menos un bufete activo.', 'danger')
             return redirect(url_for('admin_bp.listado_bufetes'))

        if _db.session.query(UsuarioSistema).filter_by(bufete_juridico_id=bufete_id, is_active=True).first():
            flash('No se puede inhabilitar el bufete porque tiene usuarios activos asociados. Desasocia o inactiva los usuarios primero.', 'danger')
            return redirect(url_for('admin_bp.listado_bufetes'))
        
        if session.get('bufete_activo_id') == bufete_id:
            flash('No se puede inhabilitar el bufete mientras esté seleccionado como el bufete activo.', 'danger')
            return redirect(url_for('admin_bp.listado_bufetes'))

        bufete.is_active = False 
        try:
            _db.session.commit()
            flash(f'Bufete "{bufete.nombre_bufete_o_razon_social}" ha sido inhabilitado exitosamente (borrado lógico).', 'success')
        except Exception as e:
            _db.session.rollback()
            flash(f'Error al inhabilitar el bufete: {e}', 'danger')
            log.error(f"Error al inhabilitar bufete: {e}", exc_info=True)
                
    return redirect(url_for('admin_bp.listado_bufetes'))


# --- Rutas de Gestión de Usuarios del Sistema ---
@admin_bp.route('/listado_usuarios_sistema')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_usuarios_sistema():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            usuarios = _db.session.query(UsuarioSistema).order_by(UsuarioSistema.nombre_usuario).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            usuarios = _db.session.query(UsuarioSistema).filter(
                UsuarioSistema.bufete_juridico_id == current_user.bufete_juridico_id,
                UsuarioSistema.rol.notin_([RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value]),
                UsuarioSistema.is_active == True 
            ).order_by(UsuarioSistema.nombre_usuario).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver usuarios del sistema.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
        
        return render_template('admin/listado_usuarios_sistema.html', title='Usuarios del Sistema', usuarios=usuarios)

@admin_bp.route('/agregar_usuario_sistema', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_usuario_sistema():
    _db = current_app.extensions['sqlalchemy']
    form = UsuarioSistemaForm()

    with current_app.app_context():
        personas = _db.session.query(Persona).filter_by(is_active=True).order_by(Persona.nombres).all()
        notarios = _db.session.query(Notario).filter_by(is_active=True).order_by(Notario.nombre_completo).all()
        
        form.persona_id.choices = [(0, 'N/A (Sin Persona Asociada)')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in personas]
        form.notario_id.choices = [(0, 'N/A (Sin Notario Asociado)')] + [(n.id, n.nombre_completo) for n in notarios]
        
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            if not current_user.bufete_juridico_id:
                flash('Tu cuenta no está asociada a un bufete. No puedes agregar usuarios sin un bufete principal.', 'danger')
                return redirect(url_for('main_bp.dashboard'))
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id, is_active=True).all()
            if not bufetes_disponibles:
                flash('Tu bufete principal no se encontró o no está activo. Contacta al Super Administrador.', 'danger')
                return redirect(url_for('main_bp.dashboard'))
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            if len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(is_active=True).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            roles_permitidos = [r.value for r in RolUsuarioSistema if r.value not in [RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value]] 
            form.rol.choices = [(r, r) for r in roles_permitidos]
        else:
            form.rol.choices = [(r.value, r.value) for r in RolUsuarioSistema]


    if form.validate_on_submit():
        with current_app.app_context():
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
                if form.rol.data in [RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value]:
                    flash('Acceso denegado: Un Administrador no puede crear usuarios con rol de Super Administrador o Administrador.', 'danger')
                    return render_template('admin/agregar_usuario_sistema.html', title='Agregar Nuevo Usuario del Sistema', form=form) 
                if form.bufete_juridico_id.data != current_user.bufete_juridico_id:
                    flash('Acceso denegado: Como Administrador, solo puedes asignar usuarios a tu propio bufete.', 'danger')
                    return render_template('admin/agregar_usuario_sistema.html', title='Agregar Nuevo Usuario del Sistema', form=form) 
            
            bufete_id_for_new_user = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            persona_id_final = form.persona_id.data if form.persona_id.data != 0 else None
            notario_id_final = form.notario_id.data if form.notario_id.data != 0 else None

            nuevo_usuario = UsuarioSistema(
                nombre_usuario=form.nombre_usuario.data,
                rol=form.rol.data,
                is_active=form.is_active.data,
                direccion_laboral=form.direccion_laboral.data,
                telefono=form.telefono.data,
                email=form.email.data,
                preferencia_contacto_red_social=form.preferencia_contacto_red_social.data,
                persona_id=persona_id_final,
                notario_id=notario_id_final,
                bufete_juridico_id=bufete_id_for_new_user
            )
            nuevo_usuario.set_password(form.password.data)

            _db.session.add(nuevo_usuario)
            try:
                _db.session.commit()
                flash('Usuario del sistema agregado exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar usuario: {e.orig}. Asegúrate de que los IDs asociados sean válidos o que el nombre de usuario/email (dentro del bufete) no exista.', 'danger')
                log.error(f"IntegrityError al agregar usuario: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al agregar el usuario del sistema: {e}', 'danger')
                log.error(f"Error general al agregar usuario: {e}", exc_info=True)

    return render_template('admin/agregar_usuario_sistema.html', title='Agregar Nuevo Usuario del Sistema', form=form)


@admin_bp.route('/editar_usuario_sistema/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_usuario_sistema(usuario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        usuario = _db.session.query(UsuarioSistema).get_or_404(usuario_id)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            if usuario.bufete_juridico_id != current_user.bufete_juridico_id:
                flash('Acceso denegado: Solo puedes editar usuarios de tu propio bufete.', 'danger')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
            if usuario.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value or (usuario.rol == RolUsuarioSistema.ADMINISTRADOR.value and usuario.id != current_user.id):
                flash('Acceso denegado: Un Administrador no puede editar Super Administradores ni otros Administradores.', 'danger')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        
        form = UsuarioSistemaForm(obj=usuario)

        personas = _db.session.query(Persona).filter_by(is_active=True).order_by(Persona.nombres).all()
        notarios = _db.session.query(Notario).filter_by(is_active=True).order_by(Notario.nombre_completo).all()
        
        form.persona_id.choices = [(0, 'N/A (Sin Persona Asociada)')] + [(p.id, f"{p.nombres} {p.apellidos}") for p in personas]
        form.notario_id.choices = [(0, 'N/A (Sin Notario Asociado)')] + [(n.id, n.nombre_completo) for n in notarios]
        
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id, is_active=True).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(is_active=True).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        if request.method == 'GET':
            if usuario.persona_id:
                form.persona_id.data = usuario.persona_id
            if usuario.notario_id:
                form.notario_id.data = usuario.notario_id
            if usuario.bufete_juridico_id:
                form.bufete_juridico_id.data = usuario.bufete_juridico_id
            else:
                form.bufete_juridico_id.data = 0 

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            roles_permitidos = [r.value for r in RolUsuarioSistema if r.value not in [RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value]]
            if usuario.id == current_user.id:
                 roles_permitidos.append(RolUsuarioSistema.ADMINISTRADOR.value)
            form.rol.choices = [(r, r) for r in roles_permitidos]
        else:
            form.rol.choices = [(r.value, r.value) for r in RolUsuarioSistema]


        if form.validate_on_submit():
            
            if form.password.data:
                usuario.set_password(form.password.data)
            
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
                if form.rol.data == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
                    flash('Acceso denegado: Un Administrador no puede asignar el rol de Super Administrador.', 'danger')
                    return render_template('admin/editar_usuario_sistema.html', title='Editar Usuario del Sistema', form=form, usuario=usuario)
                if usuario.id == current_user.id and form.rol.data != RolUsuarioSistema.ADMINISTRADOR.value:
                    flash('Acceso denegado: Un Administrador no puede cambiarse su propio rol a uno inferior. Contacta al Super Administrador.', 'danger')
                    return render_template('admin/editar_usuario_sistema.html', title='Editar Usuario del Sistema', form=form, usuario=usuario)

                if form.bufete_juridico_id.data != current_user.bufete_juridico_id:
                    flash('Acceso denegado: Como Administrador, solo puedes asignar usuarios a tu propio bufete.', 'danger')
                    return render_template('admin/editar_usuario_sistema.html', title='Editar Usuario del Sistema', form=form, usuario=usuario)
            
            usuario.persona_id = form.persona_id.data if form.persona_id.data != 0 else None
            usuario.notario_id = form.notario_id.data if form.notario_id.data != 0 else None
            usuario.bufete_juridico_id = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None

            usuario.nombre_usuario = form.nombre_usuario.data
            usuario.rol = form.rol.data
            usuario.is_active = form.is_active.data
            usuario.direccion_laboral = form.direccion_laboral.data
            usuario.telefono = form.telefono.data
            usuario.email = form.email.data
            usuario.preferencia_contacto_red_social = form.preferencia_contacto_red_social.data

            try:
                _db.session.commit()
                flash('Usuario del sistema actualizado exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar usuario: {e.orig}. Asegúrate de que los IDs asociados sean válidos o que el nombre de usuario/email (dentro del bufete) no exista.', 'danger')
                log.error(f"IntegrityError al actualizar usuario: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar el usuario del sistema: {e}', 'danger')
                log.error(f"Error general al actualizar usuario: {e}", exc_info=True)

    return render_template('admin/editar_usuario_sistema.html', title='Editar Usuario del Sistema', form=form, usuario=usuario)


@admin_bp.route('/eliminar_usuario_sistema/<int:usuario_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_usuario_sistema(usuario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        usuario = _db.session.query(UsuarioSistema).get_or_404(usuario_id)

        if current_user.id == usuario.id:
            flash('No puedes inhabilitar tu propia cuenta.', 'danger')
            return redirect(url_for('admin_bp.listado_usuarios_sistema'))

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            if usuario.bufete_juridico_id != current_user.bufete_juridico_id:
                flash('Acceso denegado: Solo puedes inhabilitar usuarios de tu propio bufete.', 'danger')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
            if usuario.rol in (RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.SUPER_ADMINISTRADOR.value):
                flash('Acceso denegado: No puedes inhabilitar a otro Administrador o Super Administrador.', 'danger')
                return redirect(url_for('admin_bp.listado_usuarios_sistema'))
        
        usuario.is_active = False 
        try:
            _db.session.commit()
            flash(f'Usuario "{usuario.nombre_usuario}" ha sido inhabilitado exitosamente (borrado lógico).', 'success')
        except Exception as e:
            _db.session.rollback()
            flash(f'Error al inhabilitar el usuario: {e}', 'danger')
            log.error(f"Error al inhabilitar usuario: {e}", exc_info=True)
        
    return redirect(url_for('admin_bp.listado_usuarios_sistema'))

# --- Rutas de Gestión de Notarios (CRUD) ---
@admin_bp.route('/listado_notarios')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_notarios():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            notarios = _db.session.query(Notario).order_by(Notario.nombre_completo).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            notarios = _db.session.query(Notario).filter_by(bufete_juridico_id=current_user.bufete_juridico_id).order_by(Notario.nombre_completo).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver notarios.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
        
        return render_template('admin/listado_notarios.html', title='Notarios', notarios=notarios)

@admin_bp.route('/agregar_notario', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_notario():
    _db = current_app.extensions['sqlalchemy']
    form = NotarioForm()

    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            if not current_user.bufete_juridico_id:
                flash('Tu cuenta no está asociada a un bufete. No puedes agregar notarios sin un bufete principal.', 'danger')
                return redirect(url_for('main_bp.dashboard'))
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id, is_active=True).all()
            if not bufetes_disponibles:
                flash('Tu bufete principal no se encontró o no está activo. Contacta al Super Administrador.', 'danger')
                return redirect(url_for('main_bp.dashboard'))
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            if len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(is_active=True).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))


    if form.validate_on_submit():
        with current_app.app_context():
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and form.bufete_juridico_id.data != current_user.bufete_juridico_id:
                flash('Acceso denegado: Como Administrador, solo puedes asignar notarios a tu propio bufete.', 'danger')
                return render_template('admin/agregar_notario.html', title='Agregar Nuevo Notario', form=form) 
            
            bufete_id_final = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None

            nuevo_notario = Notario(
                nombre_completo=form.nombre_completo.data,
                numero_colegiado=form.numero_colegiado.data,
                colegiado_activo=form.colegiado_activo.data,
                fecha_colegiado_activo_verificacion=form.fecha_colegiado_activo_verificacion.data if form.fecha_colegiado_activo_verificacion.data else None,
                firma_electronica_registrada=form.firma_electronica_registrada.data,
                proveedor_firma_electronica=form.proveedor_firma_electronica.data,
                direccion_laboral=form.direccion_laboral.data,
                telefono=form.telefono.data,
                email=form.email.data,
                preferencia_contacto_red_social=form.preferencia_contacto_red_social.data,
                bufete_juridico_id=bufete_id_final,
                is_active=form.is_active.data 
            )
            
            _db.session.add(nuevo_notario)
            try:
                _db.session.commit()
                flash('Notario agregado exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_notarios'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar notario: {e.orig}. Asegúrate de que el número de colegiado sea único o que el email (dentro del bufete) no exista.', 'danger')
                log.error(f"IntegrityError al agregar notario: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al agregar el notario: {e}', 'danger')
                log.error(f"Error general al agregar notario: {e}", exc_info=True)

    return render_template('admin/agregar_notario.html', title='Agregar Nuevo Notario', form=form)

@admin_bp.route('/editar_notario/<int:notario_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_notario(notario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        notario = _db.session.query(Notario).get_or_404(notario_id)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and notario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: Solo puedes editar notarios de tu propio bufete.', 'danger')
            return redirect(url_for('admin_bp.listado_notarios'))
        
        form = NotarioForm(obj=notario)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id, is_active=True).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            if len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
        else:
            bufetes_disponibles = _db.session.query(BufeteJuridico).filter_by(is_active=True).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
            form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        if request.method == 'GET':
            if notario.bufete_juridico_id:
                form.bufete_juridico_id.data = notario.bufete_juridico_id
            else: 
                form.bufete_juridico_id.data = 0 

        if form.validate_on_submit():
            bufete_id_final = form.bufete_juridico_id.data if form.bufete_juridico_id.data != 0 else None
            notario.bufete_juridico_id = bufete_id_final

            notario.nombre_completo = form.nombre_completo.data
            notario.numero_colegiado = form.numero_colegiado.data
            notario.colegiado_activo = form.colegiado_activo.data
            notario.fecha_colegiado_activo_verificacion = form.fecha_colegiado_activo_verificacion.data if form.fecha_colegiado_activo_verificacion.data else None
            notario.firma_electronica_registrada = form.firma_electronica_registrada.data
            notario.proveedor_firma_electronica = form.proveedor_firma_electronica.data
            notario.direccion_laboral = form.direccion_laboral.data
            notario.telefono = form.telefono.data
            notario.email = form.email.data
            notario.preferencia_contacto_red_social = form.preferencia_contacto_red_social.data
            notario.is_active = form.is_active.data 

            try:
                _db.session.commit()
                flash('Notario actualizado exitosamente.', 'success')
                return redirect(url_for('admin_bp.listado_notarios'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al actualizar notario: {e.orig}. Asegúrate de que el número de colegiado sea único o que el email (dentro del bufete) no exista.', 'danger')
                log.error(f"IntegrityError al actualizar notario: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar el notario: {e}', 'danger')
                log.error(f"Error general al actualizar notario: {e}", exc_info=True)

    return render_template('admin/editar_notario.html', title='Editar Notario', form=form, notario=notario)


@admin_bp.route('/eliminar_notario/<int:notario_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_notario(notario_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        notario = _db.session.query(Notario).get_or_404(notario_id)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and notario.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: Solo puedes eliminar notarios de tu propio bufete.', 'danger')
            return redirect(url_for('admin_bp.listado_notarios'))
        
        notario.is_active = False 
        try:
            _db.session.commit()
            flash(f'Notario "{notario.nombre_completo}" ha sido inhabilitado exitosamente (borrado lógico).', 'success')
        except Exception as e:
            _db.session.rollback()
            flash(f'Error al inhabilitar el notario: {e}', 'danger')
            log.error(f"Error al inhabilitar notario: {e}", exc_info=True)
        
    return redirect(url_for('admin_bp.listado_notarios'))

# --- Rutas de Gestión de Personas Naturales ---
@admin_bp.route('/listado_personas')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def listado_personas():
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            personas = _db.session.query(Persona).order_by(Persona.apellidos, Persona.nombres).all()
        elif current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value:
            personas = _db.session.query(Persona).filter_by(bufete_juridico_id=current_user.bufete_juridico_id, is_active=True).order_by(Persona.apellidos, Persona.nombres).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver personas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    return render_template('admin/listado_personas.html', title='Personas Naturales', personas=personas)


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
            personas_juridicas = _db.session.query(PersonaJuridica).filter_by(bufete_juridico_id=current_user.bufete_juridico_id, is_active=True).order_by(PersonaJuridica.razon_social).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver personas jurídicas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    return render_template('admin/listado_personas_juridicas.html', title='Personas Jurídicas', personas_juridicas=personas_juridicas)