# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\bienes.py
# Última Actualización: 2025-07-07 20:20:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Solución FINAL para la grabación de bienes.
#                              Se usa form.tipo_bien.data en lugar de hardcodeo.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import logging

print("==========================================================") # <-- TRACKING
print("====== TRACKING: INICIO CARGA DE app/routes/bienes.py ======") # <-- TRACKING
print("==========================================================") # <-- TRACKING

# Importar decorador de roles
from app.decorators import role_required

# Importar modelos y formularios
from app.models import db, Bien, BienInmuebleDetalle, BienMuebleDetalle, BufeteJuridico, RolUsuarioSistema
from app.forms import BienInmuebleForm, BienMuebleForm 

# Importar el procesador de contexto para acceder a la info del bufete activo
from app.context_processors import get_bufete_info

log = logging.getLogger(__name__)

# Definición del Blueprint
bienes_bp = Blueprint('bienes_bp', __name__)

# --- Rutas para Bienes ---

@bienes_bp.route('/listado')
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value, RolUsuarioSistema.PROCURADOR.value)
def listado_bienes():
    print("TRACKING: BIENES.PY - Entrando a listado_bienes()") # <--- TRACKING
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

    if not bufete_id_activo:
        flash('Por favor, selecciona un bufete para ver los bienes.', 'warning')
        return redirect(url_for('main_bp.seleccionar_bufete'))
    
    _db = current_app.extensions['sqlalchemy']
    with current_app.app_context():
        # Consultar todos los bienes (inmuebles y muebles) asociados al bufete activo
        bienes = _db.session.query(Bien).filter_by(bufete_juridico_id=bufete_id_activo).order_by(Bien.descripcion_corta).all()
        
    return render_template('bienes/listado_bienes.html', bienes=bienes, title='Gestión de Bienes')

@bienes_bp.route('/agregar_inmueble', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_inmueble():
    print("TRACKING: BIENES.PY - Entrando a agregar_inmueble()") # <--- TRACKING
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

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
        
        form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
        # Si es Super Administrador, se añade la opción de "Seleccionar Bufete" si no está ya
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and (0, '-- Seleccionar Bufete --') not in form.bufete_juridico_id.choices:
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))

        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}


    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario agregar_inmueble VALIDADO. Intentando grabar.") # <--- TRACKING
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
                    print("TRACKING: BIENES.PY - Error de unicidad detectado.") # <--- TRACKING
                    return render_template('bienes/agregar_inmueble.html', form=form, title='Agregar Nuevo Bien Inmueble')


                nuevo_inmueble = BienInmuebleDetalle(
                    tipo_bien=form.tipo_bien.data, # <--- CORREGIDO: Usar el valor del formulario
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
                print(f"TRACKING: BIENES.PY - Objeto nuevo_inmueble añadido a la sesión: {nuevo_inmueble.descripcion_corta}") # <--- TRACKING
                _db.session.commit()
                print("TRACKING: BIENES.PY - COMMIT de nuevo_inmueble realizado exitosamente.") # <--- TRACKING
                flash('Bien Inmueble agregado exitosamente!', 'success')
                return redirect(url_for('bienes_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit: {e.orig}") # <--- TRACKING
                flash(f'Error de integridad al agregar inmueble. Verifique datos únicos (ej. Finca/Folio/Libro, Registro Fiscal). ({e.orig})', 'danger')
            except Exception as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit: {e}") # <--- TRACKING
                flash(f'Ocurrió un error inesperado al agregar inmueble: {e}', 'danger')
                log.error(f"Error general al agregar inmueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario agregar_inmueble NO VALIDADO.") # <--- TRACKING
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}") # <--- AÑADIR ESTO
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}") # <--- AÑADIR ESTO
    return render_template('bienes/agregar_inmueble.html', form=form, title='Agregar Nuevo Bien Inmueble')

@bienes_bp.route('/editar_inmueble/<int:bien_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_inmueble(bien_id):
    print("TRACKING: BIENES.PY - Entrando a editar_inmueble()") # <--- TRACKING
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

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
        
        form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and (0, '-- Seleccionar Bufete --') not in form.bufete_juridico_id.choices:
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif inmueble.bufete_juridico_id: # Para SuperAdmin o si ya hay un bufete asignado
                form.bufete_juridico_id.data = inmueble.bufete_juridico_id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            else: # Si no tiene bufete asignado
                 form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario editar_inmueble VALIDADO. Intentando grabar.") # <--- TRACKING
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
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en edición.") # <--- TRACKING
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
                inmueble.ubicacion_direccion = form.ubicacion_direccion.data
                inmueble.colindancias = form.colindancias.data
                inmueble.numero_registro_fiscal = form.numero_registro_fiscal.data
                inmueble.ultimo_propietario_registral = form.ultimo_propietario_registral.data
                
                _db.session.commit()
                print("TRACKING: BIENES.PY - COMMIT de inmueble editado realizado exitosamente.") # <--- TRACKING
                flash('Bien Inmueble actualizado exitosamente!', 'success')
                return redirect(url_for('bienes_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de edición: {e.orig}") # <--- TRACKING
                flash(f'Error de integridad al actualizar inmueble. Verifique datos únicos (ej. Finca/Folio/Libro, Registro Fiscal). ({e.orig})', 'danger')
            except Exception as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit de edición: {e}") # <--- TRACKING
                flash(f'Ocurrió un error inesperado al editar inmueble: {e}', 'danger')
                log.error(f"Error general al editar inmueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario editar_inmueble NO VALIDADO.") # <--- TRACKING
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}") # <--- AÑADIR ESTO
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}") # <--- AÑADIR ESTO
    return render_template('bienes/editar_inmueble.html', form=form, title='Editar Bien Inmueble', bien=inmueble)

@bienes_bp.route('/agregar_mueble', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def agregar_mueble():
    print("TRACKING: BIENES.PY - Entrando a agregar_mueble()") # <--- TRACKING
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

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
        
        form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and (0, '-- Seleccionar Bufete --') not in form.bufete_juridico_id.choices:
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif bufete_id_activo: # Para SuperAdmin o si ya hay un bufete activo
                form.bufete_juridico_id.data = bufete_id_activo
                form.bufete_juridico_id.render_kw = {'readonly': True}

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario agregar_mueble VALIDADO. Intentando grabar.") # <--- TRACKING
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
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en agregar mueble.") # <--- TRACKING
                    return render_template('bienes/agregar_mueble.html', form=form, title='Agregar Nuevo Bien Mueble')

                nuevo_mueble = BienMuebleDetalle(
                    tipo_bien=form.tipo_bien.data, # <--- CORREGIDO: Usar el valor del formulario
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
                print(f"TRACKING: BIENES.PY - Objeto nuevo_mueble añadido a la sesión: {nuevo_mueble.descripcion_corta}") # <--- TRACKING
                _db.session.commit()
                print("TRACKING: BIENES.PY - COMMIT de nuevo_mueble realizado exitosamente.") # <--- TRACKING
                flash('Bien Mueble agregado exitosamente!', 'success')
                return redirect(url_for('bienes_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de agregar mueble: {e.orig}") # <--- TRACKING
                flash(f'Error de integridad al agregar mueble. Verifique datos únicos (ej. Número de Placa, VIN). ({e.orig})', 'danger')
            except Exception as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit de agregar mueble: {e}") # <--- TRACKING
                flash(f'Ocurrió un error inesperado al agregar mueble: {e}', 'danger')
                log.error(f"Error general al agregar mueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario agregar_mueble NO VALIDADO.") # <--- TRACKING
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}") # <--- AÑADIR ESTO
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}") # <--- AÑADIR ESTO
    return render_template('bienes/agregar_mueble.html', form=form, title='Agregar Nuevo Bien Mueble')

@bienes_bp.route('/editar_mueble/<int:bien_id>', methods=['GET', 'POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def editar_mueble(bien_id):
    print("TRACKING: BIENES.PY - Entrando a editar_mueble()") # <--- TRACKING
    bufete_info_data = get_bufete_info().get('bufete_info')
    bufete_id_activo = bufete_info_data.get('id') if bufete_info_data else None

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
        
        form.bufete_juridico_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes_disponibles]
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value and (0, '-- Seleccionar Bufete --') not in form.bufete_juridico_id.choices:
            form.bufete_juridico_id.choices.insert(0, (0, '-- Seleccionar Bufete --'))
        
        # Pre-llenar y hacer de solo lectura el campo de bufete_juridico_id
        if hasattr(form, 'bufete_juridico_id'):
            if current_user.rol == RolUsuarioSistema.ADMINISTRADOR.value and len(bufetes_disponibles) == 1:
                form.bufete_juridico_id.data = bufetes_disponibles[0].id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            elif mueble.bufete_juridico_id: # Para SuperAdmin o si ya hay un bufete asignado
                form.bufete_juridico_id.data = mueble.bufete_juridico_id
                form.bufete_juridico_id.render_kw = {'readonly': True}
            else: # Si no tiene bufete asignado
                 form.bufete_juridico_id.data = 0 # Asigna la opción "N/A"

    if form.validate_on_submit():
        print("TRACKING: BIENES.PY - Formulario editar_mueble VALIDADO. Intentando grabar.") # <--- TRACKING
        _db = current_app.extensions['sqlalchemy']
        with current_app.app_context():
            try:
                # Validación de unicidad para otros muebles (excluyendo el que se está editando)
                existing_mueble = _db.session.query(BienMuebleDetalle).filter(
                    ((BienMuebleDetalle.numero_placa == form.numero_placa.data) | \
                    (BienMuebleDetalle.numero_identificacion_vehicular_vin == form.numero_identificacion_vehicular_vin.data)),
                    BienMuebleDetalle.bufete_juridico_id == bufete_id_activo,
                    BienMuebleDetalle.id != bien_id
                ).first()
                if existing_mueble:
                    flash(f'Error: Ya existe otro mueble con la misma placa o VIN para este bufete.', 'danger')
                    print("TRACKING: BIENES.PY - Error de unicidad detectado en edición de mueble.") # <--- TRACKING
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
                print("TRACKING: BIENES.PY - COMMIT de mueble editado realizado exitosamente.") # <--- TRACKING
                flash('Bien Mueble actualizado exitosamente!', 'success')
                return redirect(url_for('bienes_bp.listado_bienes'))
            except IntegrityError as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - IntegrityError durante commit de edición de mueble: {e.orig}") # <--- TRACKING
                flash(f'Error de integridad al actualizar mueble. Verifique datos únicos (ej. Número de Placa, VIN). ({e.orig})', 'danger')
            except Exception as e:
                _db.session.rollback()
                print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit de edición de mueble: {e}") # <--- TRACKING
                flash(f'Ocurrió un error inesperado al editar mueble: {e}', 'danger')
                log.error(f"Error general al editar mueble: {e}", exc_info=True)
    else:
        print("TRACKING: BIENES.PY - Formulario editar_mueble NO VALIDADO.") # <--- TRACKING
        print(f"TRACKING: BIENES.PY - Errores del formulario: {form.errors}") # <--- AÑADIR ESTO
        print(f"TRACKING: BIENES.PY - Datos del formulario: {form.data}") # <--- AÑADIR ESTO
    return render_template('bienes/editar_mueble.html', form=form, title='Editar Bien Mueble', bien=mueble)

@bienes_bp.route('/eliminar/<int:bien_id>', methods=['POST'])
@login_required
@role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
def eliminar_bien(bien_id):
    print("TRACKING: BIENES.PY - Entrando a eliminar_bien()") # <--- TRACKING
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
            print(f"TRACKING: BIENES.PY - Objeto bien eliminado de la sesión: {bien.descripcion_corta}") # <--- TRACKING
            _db.session.commit()
            print("TRACKING: BIENES.PY - COMMIT de eliminación de bien realizado exitosamente.") # <--- TRACKING
            flash('Bien eliminado exitosamente!', 'success')
        except IntegrityError as e:
            _db.session.rollback()
            print(f"TRACKING: BIENES.PY - IntegrityError durante commit de eliminación: {e.orig}") # <--- TRACKING
            flash(f'No se puede eliminar el bien porque está asociado a otros registros (ej. documentos). ({e.orig})', 'danger')
        except Exception as e:
            _db.session.rollback()
            print(f"TRACKING: BIENES.PY - Excepción inesperada durante commit de eliminación: {e}") # <--- TRACKING
            flash(f'Ocurrió un error al eliminar el bien: {e}', 'danger')
            log.error(f"Error general al eliminar bien: {e}", exc_info=True)
    return redirect(url_for('bienes_bp.listado_bienes'))