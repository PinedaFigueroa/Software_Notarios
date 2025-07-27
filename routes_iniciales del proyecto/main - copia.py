# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\main.py
# Última Actualización: 2025-07-06 14:15:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Corrección de mensaje flash (guion bajo) y favicon.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from app.models import db, DocumentoNotarial, UsuarioSistema, BufeteJuridico 
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app.forms import LoginForm, RegistrationForm 
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
import sys


main_bp = Blueprint('main_bp', __name__) 

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required 
def dashboard():
    # Después de loguearse, si no hay bufete activo en sesión, redirigir a la selección de bufete.
    if 'bufete_activo_id' not in session:
        return redirect(url_for('main_bp.seleccionar_bufete'))

    # Renderiza la plantilla que está en templates/main/dashboard.html
    return render_template('main/dashboard.html', title='Dashboard Principal del Sistema Notarial')

# --- Rutas de Autenticación ---
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # ¡CRUCIAL! Forzar contexto de aplicación para la consulta a la base de datos
        _db_instance = current_app.extensions['sqlalchemy'] # Obtener la instancia de db desde la extensión
        with current_app.app_context(): # Asegurar que la consulta se haga en el contexto correcto
            user = _db_instance.session.query(UsuarioSistema).filter_by(nombre_usuario=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o contraseña inválidos.', 'danger')
            return redirect(url_for('main_bp.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Redirige a selección de bufete para asegurar que se elija un bufete activo
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main_bp.seleccionar_bufete')) 
    
    # Renderiza la plantilla que está en templates/main/login.html
    return render_template('main/login.html', title='Iniciar Sesión', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('bufete_activo_id', None) # Limpiar el bufete_id de la sesión
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('main_bp.login'))

# ================================================================
# RUTA DE REGISTRO PÚBLICO DESHABILITADA POR SEGURIDAD Y CONTROL
# Los usuarios deben ser creados por un administrador interno.
# ================================================================
# @main_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main_bp.dashboard'))
    
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = UsuarioSistema(nombre_usuario=form.username.data, rol='Procurador', is_active=True)
#         user.set_password(form.password.data)
        
#         primer_bufete = BufeteJuridico.query.first()
#         if primer_bufete:
#             user.bufete_juridico_id = primer_bufete.id
#         else:
#             flash('No hay bufetes registrados. No es posible registrar usuarios por esta vía sin un bufete inicial. Contacta al administrador.', 'danger')
#             return render_template('main/register.html', title='Registrar Usuario', form=form)

#         try:
#             db.session.add(user)
#             db.session.commit()
#             flash('Usuario registrado exitosamente! Ahora, inicie sesión.', 'success')
#             return redirect(url_for('main_bp.login'))
#         except IntegrityError:
#             db.session.rollback()
#             flash(f'El nombre de usuario ya está en uso.', 'danger')
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error al registrar usuario: {e}', 'danger')
#             print(f"Error al registrar usuario: {e}", file=sys.stderr)
#     return render_template('main/register.html', title='Registrar Usuario', form=form)
# ================================================================


@main_bp.route('/seleccionar_bufete', methods=['GET', 'POST'])
@login_required
def seleccionar_bufete():
    # Creamos un formulario en línea para la selección del bufete
    class SelectBufeteForm(FlaskForm):
        bufete_id = SelectField('Bufete', coerce=int, validators=[DataRequired()])
        submit = SubmitField('Acceder al Bufete')

    form = SelectBufeteForm() # Instancia del formulario

    # ¡CRUCIAL! Forzar contexto de aplicación para la consulta a la base de datos
    _db_instance = current_app.extensions['sqlalchemy'] # Obtener la instancia de db desde la extensión
    with current_app.app_context(): # Asegurar que la consulta se haga en el contexto correcto
        # Lógica para mostrar bufetes basados en el rol del usuario
        if current_user.rol == 'Super Administrador':
            bufetes = _db_instance.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
        else:
            bufetes = _db_instance.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
        
        # Redirige si el usuario normal solo tiene acceso a un bufete y no hay bufete activo en sesión
        if len(bufetes) == 1 and request.method == 'GET' and 'bufete_activo_id' not in session:
            session['bufete_activo_id'] = bufetes[0].id
            flash(f'Bufete activo seleccionado: {bufetes[0].nombre_bufete_o_razon_social}', 'success') # SIN DEBUG
            return redirect(url_for('main_bp.dashboard'))
        
        if not bufetes:
            flash('No hay bufetes disponibles para tu usuario. Por favor, contacta al administrador.', 'warning')
            logout_user()
            return redirect(url_for('main_bp.login'))

        # Asignar las opciones al campo del formulario.
        form.bufete_id.choices = [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes]
        form.bufete_id.choices.insert(0, (0, '-- Seleccionar un bufete --')) # Opción por defecto
        
        if form.validate_on_submit():
            bufete_id = form.bufete_id.data
            if bufete_id: 
                if current_user.rol != 'Super Administrador' and int(bufete_id) != current_user.bufete_juridico_id:
                    flash('Acceso denegado al bufete seleccionado.', 'danger')
                    return redirect(url_for('main_bp.seleccionar_bufete'))
                
                session['bufete_activo_id'] = int(bufete_id)
                # ¡CRUCIAL! Forzar contexto de aplicación para la consulta a la base de datos
                # Asegurarse de que la consulta para el nombre del bufete también use el contexto explícito
                bufete_seleccionado_nombre = _db_instance.session.query(BufeteJuridico).get(int(bufete_id)).nombre_bufete_o_razon_social
                flash(f"Bufete activo seleccionado: {bufete_seleccionado_nombre}", 'success') # SIN DEBUG
                return redirect(url_for('main_bp.dashboard'))
            else:
                flash('Por favor, selecciona un bufete.', 'danger')
        
        selected_bufete_id = session.get('bufete_activo_id')
        return render_template('main/seleccionar_bufete.html', title='Seleccionar Bufete', form=form, bufetes=bufetes, selected_bufete_id=selected_bufete_id)

# Función auxiliar para obtener el ID del bufete activo desde la sesión
def get_bufete_activo_id_from_session():
    return session.get('bufete_activo_id')