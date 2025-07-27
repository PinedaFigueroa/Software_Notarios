# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\clausulas.py
# Última Actualización: 2025-07-07 13:00:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Lógica de DB y bufete activo robustecida, decoradores de rol, manejo de errores.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from sqlalchemy.exc import IntegrityError
import logging
from flask_login import login_required, current_user # Importar current_user
from app.decorators import role_required # Importar el decorador de roles

# Importar modelos y formularios
from app.models import db, Clausula, BufeteJuridico, RolUsuarioSistema # Asegúrate de que db esté disponible o se acceda vía extension
from app.forms import ClausulaForm 

# Importar el procesador de contexto para acceder a la info del bufete activo
from app.context_processors import get_bufete_info

log = logging.getLogger(__name__)

# Definición del Blueprint
clausulas_bp = Blueprint('clausulas_bp', __name__)

# Función auxiliar para obtener la información del bufete activo de forma robusta
# Ya no se necesita una función auxiliar aquí si usamos get_bufete_info() directamente.

# Ruta para listar todas las cláusulas
@clausulas_bp.route('/')
@clausulas_bp.route('/listado')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.PROCURADOR.value) # Asumiendo que procuradores pueden ver.
def listado_clausulas():
    bufete_info_data = get_bufete_info().get('bufete_info') # Obtener el diccionario del bufete activo
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para gestionar Cláusulas. (Error: No hay bufete activo en sesión)', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    _db = current_app.extensions['sqlalchemy'] # Acceso robusto a la DB
    with current_app.app_context(): # Asegurar contexto para la consulta
        clausulas = _db.session.query(Clausula).filter_by(bufete_juridico_id=bufete_id_activo).order_by(Clausula.nombre_clausula).all()
        
    return render_template('clausulas/listado_clausulas.html', clausulas=clausulas, title='Biblioteca de Cláusulas')

# Ruta para agregar una cláusula
@clausulas_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value) # Asumiendo que solo Admin/SuperAdmin pueden agregar
def agregar_clausula():
    form = ClausulaForm()
    
    # Obtener el bufete activo para asignar la cláusula
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para agregar Cláusulas. (Error: No hay bufete activo en sesión)', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))

    if form.validate_on_submit():
        _db = current_app.extensions['sqlalchemy'] # Acceso robusto a la DB
        with current_app.app_context(): # Asegurar contexto para la DB
            # Verificar si ya existe una cláusula con el mismo nombre para ESTE BUFETE
            existing_clausula = _db.session.query(Clausula).filter_by(
                nombre_clausula=form.nombre_clausula.data,
                bufete_juridico_id=bufete_id_activo
            ).first()
            if existing_clausula:
                flash(f'Error: Ya existe una cláusula con el nombre "{form.nombre_clausula.data}" para este bufete.', 'danger')
                return render_template('clausulas/agregar_clausula.html', form=form, title='Agregar Cláusula')

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
                bufete_juridico_id=bufete_id_activo # Asignar al bufete activo
            )
            _db.session.add(nueva_clausula)
            try:
                _db.session.commit()
                flash('Cláusula agregada exitosamente!', 'success')
                return redirect(url_for('clausulas_bp.listado_clausulas'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al agregar cláusula. Verifique datos únicos. ({e.orig})', 'danger')
                log.error(f"IntegrityError al agregar cláusula: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al agregar cláusula: {e}', 'danger')
                log.error(f"Error inesperado al agregar cláusula: {e}", exc_info=True)
    
    return render_template('clausulas/agregar_clausula.html', form=form, title='Agregar Cláusula')

# Ruta para editar una cláusula
@clausulas_bp.route('/editar/<int:clausula_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value) # Asumiendo que solo Admin/SuperAdmin pueden editar
def editar_clausula(clausula_id):
    _db = current_app.extensions['sqlalchemy'] # Acceso robusto a la DB
    with current_app.app_context(): # Asegurar contexto para la DB
        clausula = _db.session.query(Clausula).get_or_404(clausula_id)

        # Verificar que la cláusula pertenezca al bufete activo
        bufete_info_data = get_bufete_info().get('bufete_info')
        bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

        if not bufete_id_activo or clausula.bufete_juridico_id != bufete_id_activo:
            flash('Acceso denegado o cláusula no encontrada para este bufete.', 'danger')
            return redirect(url_for('clausulas_bp.listado_clausulas'))

        form = ClausulaForm(obj=clausula) # Pre-rellenar formulario con datos existentes
        if form.validate_on_submit():
            # Verificar si ya existe otra cláusula con el mismo nombre para ESTE BUFETE (excluyendo la que se está editando)
            existing_clausula = _db.session.query(Clausula).filter(
                Clausula.nombre_clausula == form.nombre_clausula.data,
                Clausula.bufete_juridico_id == bufete_id_activo,
                Clausula.id != clausula_id
            ).first()
            if existing_clausula:
                flash(f'Error: Ya existe otra cláusula con el nombre "{form.nombre_clausula.data}" para este bufete.', 'danger')
                return render_template('clausulas/editar_clausula.html', form=form, title='Editar Cláusula', clausula=clausula)


            clausula.nombre_clausula = form.nombre_clausula.data
            clausula.contenido_base = form.contenido_base.data
            clausula.tipo_clausula = form.tipo_clausula.data
            clausula.tags = form.tags.data
            clausula.editable = form.editable.data
            clausula.fundamentacion_doctrinal_observaciones = form.fundamentacion_doctrinal_observaciones.data
            clausula.fundamentacion_legal_articulos = form.fundamentacion_legal_articulos.data
            clausula.obligatoriedad_sugerencia = form.obligatoriedad_sugerencia.data
            clausula.aplica_a_instrumentos_publicos = form.aplica_a_instrumentos_publicos.data

            try:
                _db.session.commit()
                flash('Cláusula actualizada exitosamente!', 'success')
                return redirect(url_for('clausulas_bp.listado_clausulas'))
            except IntegrityError as e:
                _db.session.rollback()
                flash(f'Error de integridad al editar cláusula. Verifique datos únicos. ({e.orig})', 'danger')
                log.error(f"IntegrityError al editar cláusula: {e}", exc_info=True)
            except Exception as e:
                _db.session.rollback()
                flash(f'Ocurrió un error inesperado al editar cláusula: {e}', 'danger')
                log.error(f"Error inesperado al editar cláusula: {e}", exc_info=True)
    
    return render_template('clausulas/editar_clausula.html', form=form, title='Editar Cláusula', clausula=clausula)

# Ruta para eliminar una cláusula
@clausulas_bp.route('/eliminar/<int:clausula_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value) # Asumiendo que solo Admin/SuperAdmin pueden eliminar
def eliminar_clausula(clausula_id):
    _db = current_app.extensions['sqlalchemy'] # Acceso robusto a la DB
    with current_app.app_context(): # Asegurar contexto para la DB
        clausula = _db.session.query(Clausula).get_or_404(clausula_id)
        
        # Verificar que la cláusula pertenezca al bufete activo
        bufete_info_data = get_bufete_info().get('bufete_info')
        bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

        if not bufete_id_activo or clausula.bufete_juridico_id != bufete_id_activo:
            flash('Acceso denegado o cláusula no encontrada para este bufete.', 'danger')
            return redirect(url_for('clausulas_bp.listado_clausulas'))

        try:
            _db.session.delete(clausula)
            _db.session.commit()
            flash('Cláusula eliminada exitosamente!', 'success')
        except IntegrityError as e: # Capturar IntegrityError específicamente para relaciones
            _db.session.rollback()
            flash(f'No se puede eliminar la cláusula porque está asociada a otros registros (ej. documentos).', 'danger')
            log.error(f"IntegrityError al eliminar cláusula: {e}", exc_info=True)
        except Exception as e:
            _db.session.rollback()
            flash(f'Error al eliminar cláusula: {e}', 'danger')
            log.error(f"Error general al eliminar cláusula: {e}", exc_info=True)
            
    return redirect(url_for('clausulas_bp.listado_clausulas'))