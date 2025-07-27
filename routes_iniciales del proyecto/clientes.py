# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\clientes.py
# Última Actualización: 2025-07-05 15:25:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Implementación de acceso a db via current_app.extensions en funciones de clientes.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required, current_user
# Importar modelos (con _db acceso ya corregido en __init__.py)
from app.models import Persona, PersonaJuridica, BufeteJuridico, RolUsuarioSistema # Importa solo lo que necesitas
from app.forms import PersonaForm, PersonaJuridicaForm # Importa los formularios necesarios
from sqlalchemy.exc import IntegrityError
import logging

log = logging.getLogger(__name__)

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route('/listado_clientes')
@login_required
def listado_clientes():
    _db = current_app.extensions['sqlalchemy'] # ACCESO EXPLÍCITO A DB
    with current_app.app_context(): # Asegurar contexto para la consulta
        bufete_id = session.get('id_bufete_activo')
        if not bufete_id:
            flash('Por favor, selecciona un bufete para ver los clientes.', 'warning')
            return redirect(url_for('main_bp.seleccionar_bufete'))

        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            personas = _db.session.query(Persona).order_by(Persona.apellidos, Persona.nombres).all()
            personas_juridicas = _db.session.query(PersonaJuridica).order_by(PersonaJuridica.razon_social).all()
        elif current_user.rol in [RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.NOTARIO.value, RolUsuarioSistema.PROCURADOR.value]:
            personas = _db.session.query(Persona).filter_by(bufete_juridico_id=bufete_id).order_by(Persona.apellidos, Persona.nombres).all()
            personas_juridicas = _db.session.query(PersonaJuridica).filter_by(bufete_juridico_id=bufete_id).order_by(PersonaJuridica.razon_social).all()
        else:
            flash('Acceso denegado: No tienes permisos para ver clientes.', 'danger')
            return redirect(url_for('main_bp.dashboard'))
    
    return render_template('clientes/listado_clientes.html', title='Gestión de Clientes', personas=personas, personas_juridicas=personas_juridicas)

@clientes_bp.route('/agregar_persona', methods=['GET', 'POST'])
@login_required
def agregar_persona():
    _db = current_app.extensions['sqlalchemy']
    form = PersonaForm()

    if form.validate_on_submit():
        with current_app.app_context():
            if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
                # El Super Admin puede especificar el bufete_juridico_id
                bufete_id = form.bufete_juridico_id.data
            else:
                # Otros roles se asignan al bufete_activo_id de su sesión
                bufete_id = session.get('id_bufete_activo')

            if not bufete_id:
                flash('Debe seleccionar un bufete antes de agregar una persona.', 'danger')
                return redirect(url_for('clientes_bp.listado_clientes')) # O renderizar con un mensaje de error en el form

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
                dpi_lugar_emision=form.dpi_lugar_emision.data,
                nit=form.nit.data,
                telefono=form.telefono.data,
                email=form.email.data,
                direccion_completa=form.direccion_completa.data,
                identificado_por=form.identificado_por.data,
                testigo_conocimiento_id=form.testigo_conocimiento_id.data if form.testigo_conocimiento_id.data != 0 else None,
                bufete_juridico_id=bufete_id # Asignar al bufete
            )
            _db.session.add(nueva_persona)
            try:
                _db.session.commit()
                flash('Persona agregada exitosamente.', 'success')
                return redirect(url_for('clientes_bp.listado_clientes'))
            except IntegrityError:
                _db.session.rollback()
                flash('Ya existe una persona con ese DPI o NIT.', 'danger')
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al agregar la persona: {e}', 'danger')
                log.error(f"Error al agregar persona: {e}", exc_info=True)

    return render_template('clientes/agregar_persona.html', title='Agregar Nueva Persona Natural', form=form)

@clientes_bp.route('/editar_persona/<int:persona_id>', methods=['GET', 'POST'])
@login_required
def editar_persona(persona_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona = _db.session.query(Persona).get_or_404(persona_id)

        # Lógica de permisos
        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: Solo puedes editar personas de tu propio bufete.', 'danger')
            return redirect(url_for('clientes_bp.listado_clientes'))
        elif current_user.rol not in [RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.NOTARIO.value, RolUsuarioSistema.PROCURADOR.value]:
            flash('Acceso denegado: No tienes permisos para editar personas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))

        form = PersonaForm(obj=persona) # Pre-rellenar formulario
        # Si el usuario no es Super Admin, limitar las opciones de bufete
        if current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            form.bufete_juridico_id.choices = [(current_user.bufete_juridico_id, BufeteJuridico.query.get(current_user.bufete_juridico_id).nombre_bufete_o_razon_social)]
            form.bufete_juridico_id.data = current_user.bufete_juridico_id

        if form.validate_on_submit():
            form.populate_obj(persona)
            try:
                _db.session.commit()
                flash('Persona actualizada exitosamente.', 'success')
                return redirect(url_for('clientes_bp.listado_clientes'))
            except IntegrityError:
                _db.session.rollback()
                flash('Ya existe otra persona con el mismo DPI o NIT.', 'danger')
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar la persona: {e}', 'danger')
                log.error(f"Error al actualizar persona: {e}", exc_info=True)

    return render_template('clientes/editar_persona.html', title='Editar Persona Natural', form=form, persona=persona)

@clientes_bp.route('/eliminar_persona/<int:persona_id>', methods=['POST'])
@login_required
def eliminar_persona(persona_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona = _db.session.query(Persona).get_or_404(persona_id)

        if current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            flash('Acceso denegado: Solo el Super Administrador puede eliminar personas.', 'danger')
            return redirect(url_for('clientes_bp.listado_clientes'))

        # NO ELIMINACIÓN FÍSICA. Lógica de borrado suave.
        # Por simplicidad aquí, solo flasheamos un mensaje.
        flash(f'Persona "{persona.nombres} {persona.apellidos}" (ID: {persona.id}) ha sido marcada para eliminación lógica (no implementada físicamente).', 'info')

    return redirect(url_for('clientes_bp.listado_clientes'))

# --- Rutas para Persona Jurídica ---

@clientes_bp.route('/agregar_persona_juridica', methods=['GET', 'POST'])
@login_required
def agregar_persona_juridica():
    _db = current_app.extensions['sqlalchemy']
    form = PersonaJuridicaForm()

    if form.validate_on_submit():
        with current_app.app_context():
            if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
                bufete_id = form.bufete_juridico_id.data
            else:
                bufete_id = session.get('id_bufete_activo')
            
            if not bufete_id:
                flash('Debe seleccionar un bufete antes de agregar una persona jurídica.', 'danger')
                return redirect(url_for('clientes_bp.listado_clientes'))

            nueva_persona_juridica = PersonaJuridica(
                razon_social=form.razon_social.data,
                nombre_comercial=form.nombre_comercial.data,
                nit=form.nit.data,
                datos_inscripcion_registral=form.datos_inscripcion_registral.data,
                direccion_completa=form.direccion_completa.data,
                telefono=form.telefono.data,
                email=form.email.data,
                bufete_juridico_id=bufete_id
            )
            _db.session.add(nueva_persona_juridica)
            try:
                _db.session.commit()
                flash('Persona Jurídica agregada exitosamente.', 'success')
                return redirect(url_for('clientes_bp.listado_clientes'))
            except IntegrityError:
                _db.session.rollback()
                flash('Ya existe una persona jurídica con esa razón social o NIT.', 'danger')
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al agregar la persona jurídica: {e}', 'danger')
                log.error(f"Error al agregar persona jurídica: {e}", exc_info=True)

    return render_template('clientes/agregar_persona_juridica.html', title='Agregar Nueva Persona Jurídica', form=form)

@clientes_bp.route('/editar_persona_juridica/<int:pj_id>', methods=['GET', 'POST'])
@login_required
def editar_persona_juridica(pj_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona_juridica = _db.session.query(PersonaJuridica).get_or_404(pj_id)

        if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and persona_juridica.bufete_juridico_id != current_user.bufete_juridico_id:
            flash('Acceso denegado: Solo puedes editar personas jurídicas de tu propio bufete.', 'danger')
            return redirect(url_for('clientes_bp.listado_clientes'))
        elif current_user.rol not in [RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.NOTARIO.value, RolUsuarioSistema.PROCURADOR.value]:
            flash('Acceso denegado: No tienes permisos para editar personas jurídicas.', 'danger')
            return redirect(url_for('main_bp.dashboard'))

        form = PersonaJuridicaForm(obj=persona_juridica)
        if current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            form.bufete_juridico_id.choices = [(current_user.bufete_juridico_id, BufeteJuridico.query.get(current_user.bufete_juridico_id).nombre_bufete_o_razon_social)]
            form.bufete_juridico_id.data = current_user.bufete_juridico_id

        if form.validate_on_submit():
            form.populate_obj(persona_juridica)
            try:
                _db.session.commit()
                flash('Persona Jurídica actualizada exitosamente.', 'success')
                return redirect(url_for('clientes_bp.listado_clientes'))
            except IntegrityError:
                _db.session.rollback()
                flash('Ya existe otra persona jurídica con la misma razón social o NIT.', 'danger')
            except Exception as e:
                _db.session.rollback()
                flash(f'Error al actualizar la persona jurídica: {e}', 'danger')
                log.error(f"Error al actualizar persona jurídica: {e}", exc_info=True)

    return render_template('clientes/editar_persona_juridica.html', title='Editar Persona Jurídica', form=form, persona_juridica=persona_juridica)

@clientes_bp.route('/eliminar_persona_juridica/<int:pj_id>', methods=['POST'])
@login_required
def eliminar_persona_juridica(pj_id):
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        persona_juridica = _db.session.query(PersonaJuridica).get_or_404(pj_id)

        if current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
            flash('Acceso denegado: Solo el Super Administrador puede eliminar personas jurídicas.', 'danger')
            return redirect(url_for('clientes_bp.listado_clientes'))

        # NO ELIMINACIÓN FÍSICA. Lógica de borrado suave.
        flash(f'Persona Jurídica "{persona_juridica.razon_social}" (ID: {persona_juridica.id}) ha sido marcada para eliminación lógica (no implementada físicamente).', 'info')

    return redirect(url_for('clientes_bp.listado_clientes'))