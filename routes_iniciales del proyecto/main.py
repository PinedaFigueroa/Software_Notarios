# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\main.py
# Última Actualización: 2025-07-10 21:30:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Añadidos prints de depuración para entender redirecciones,
#                              Asegurado redirección al dashboard tras selección de bufete.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
# Importar solo los modelos que están en core_models.py
from app.models.core_models import db, UsuarioSistema, BufeteJuridico
from app.models.enums import RolUsuarioSistema
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from urllib.parse import urlparse # Asegúrate de que urlparse esté importado aquí

from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
import sys

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    print("DEBUG: main_bp.dashboard - Entrando a dashboard.")
    # Después de loguearse, si no hay bufete activo en sesión, redirigir a la selección de bufete.
    if 'bufete_activo_id' not in session:
        print("DEBUG: main_bp.dashboard - No hay bufete activo en sesión. Redirigiendo a seleccionar_bufete.")
        return redirect(url_for('main_bp.seleccionar_bufete'))

    print(f"DEBUG: main_bp.dashboard - Bufete activo ID: {session.get('bufete_activo_id')}. Renderizando dashboard.html.")
    # Renderiza la plantilla que está en templates/main/dashboard.html
    return render_template('main/dashboard.html', title='Dashboard Principal')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("DEBUG: main_bp.login - Usuario ya autenticado. Redirigiendo a dashboard.")
        return redirect(url_for('main_bp.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        _db_instance = current_app.extensions['sqlalchemy']
        with current_app.app_context(): # Asegurar contexto para la consulta
            user = _db_instance.session.query(UsuarioSistema).filter_by(nombre_usuario=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o contraseña inválidos', 'danger')
            print("DEBUG: main_bp.login - Credenciales inválidas.")
            return redirect(url_for('main_bp.login'))

        login_user(user, remember=form.remember_me.data)
        print(f"DEBUG: main_bp.login - Usuario '{user.nombre_usuario}' logueado exitosamente.")

        # Después de loguearse, si no hay bufete activo en sesión, redirigir a la selección de bufete.
        # Esto es importante para el flujo inicial.
        if 'bufete_activo_id' not in session or session.get('bufete_activo_id') is None:
            print("DEBUG: main_bp.login - No hay bufete activo tras login. Redirigiendo a seleccionar_bufete.")
            return redirect(url_for('main_bp.seleccionar_bufete'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_bp.dashboard')
        print(f"DEBUG: main_bp.login - Redirigiendo a next_page: {next_page}")
        return redirect(next_page)

    return render_template('main/login.html', title='Iniciar Sesión', form=form)


@main_bp.route('/logout')
@login_required
def logout():
    print("DEBUG: main_bp.logout - Cerrando sesión y limpiando bufete activo.")
    session.pop('bufete_activo_id', None) # Limpiar el bufete activo al cerrar sesión
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main_bp.login'))


class SeleccionarBufeteForm(FlaskForm):
    bufete_id = SelectField('Seleccionar Bufete', coerce=int, validators=[DataRequired('Este campo es obligatorio.')])
    submit = SubmitField('Seleccionar')

@main_bp.route('/seleccionar_bufete', methods=['GET', 'POST'])
@login_required
def seleccionar_bufete():
    _db_instance = current_app.extensions['sqlalchemy'] # ACCESO EXPLÍCITO A DB
    with current_app.app_context(): # Asegurar contexto para la consulta
        if current_user.rol == RolUsuarioSistema.SUPER_ADMINISTRADOR.value: # Usar .value para comparar con string en Enum
            bufetes = _db_instance.session.query(BufeteJuridico).order_by(BufeteJuridico.nombre_bufete_o_razon_social).all()
        else:
            # Si no es Super Administrador, solo puede ver su propio bufete
            bufetes = _db_instance.session.query(BufeteJuridico).filter_by(id=current_user.bufete_juridico_id).all()
            if not bufetes:
                flash('No tienes un bufete asignado. Contacta al administrador.', 'danger')
                print("DEBUG: main_bp.seleccionar_bufete - Usuario sin bufete asignado. Redirigiendo a logout.")
                return redirect(url_for('main_bp.logout')) # O a una página de error/contacto

    # Asegurarse de que las choices se pasen correctamente al formulario
    form = SeleccionarBufeteForm()
    # Si solo hay un bufete y el usuario no es Super Administrador, preseleccionar y deshabilitar
    if len(bufetes) == 1 and current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value:
        form.bufete_id.choices = [(bufetes[0].id, bufetes[0].nombre_bufete_o_razon_social)]
        form.bufete_id.data = bufetes[0].id
        form.bufete_id.render_kw = {'readonly': True, 'disabled': True} # Hacerlo no editable en frontend
    else:
        form.bufete_id.choices = [(0, '-- Seleccionar un bufete --')] + [(b.id, b.nombre_bufete_o_razon_social) for b in bufetes]

    if form.validate_on_submit():
        bufete_id = form.bufete_id.data
        if bufete_id and bufete_id != 0: # Asegurarse de que no sea la opción "Seleccionar un bufete"
            if current_user.rol != RolUsuarioSistema.SUPER_ADMINISTRADOR.value and int(bufete_id) != current_user.bufete_juridico_id:
                flash('Acceso denegado al bufete seleccionado.', 'danger')
                print(f"DEBUG: main_bp.seleccionar_bufete - Acceso denegado. Rol: {current_user.rol}, Bufete seleccionado: {bufete_id}, Bufete usuario: {current_user.bufete_juridico_id}")
                return redirect(url_for('main_bp.seleccionar_bufete'))

            session['bufete_activo_id'] = int(bufete_id)
            # Asegurarse de que la consulta para el nombre del bufete también use el contexto explícito
            bufete_seleccionado_nombre = _db_instance.session.query(BufeteJuridico).get(int(bufete_id)).nombre_bufete_o_razon_social
            flash(f"Bufete activo seleccionado: {bufete_seleccionado_nombre}", 'success')
            print(f"DEBUG: main_bp.seleccionar_bufete - Bufete '{bufete_seleccionado_nombre}' (ID: {bufete_id}) seleccionado y guardado en sesión.")
            return redirect(url_for('main_bp.dashboard')) # REDIRIGIR SIEMPRE AL DASHBOARD

        else:
            flash('Por favor, selecciona un bufete válido.', 'danger')
            print("DEBUG: main_bp.seleccionar_bufete - Selección de bufete inválida (ID 0 o None).")

    selected_bufete_id = session.get('bufete_activo_id')
    print(f"DEBUG: main_bp.seleccionar_bufete - Renderizando seleccionar_bufete.html. Bufete activo actual en sesión: {selected_bufete_id}")
    return render_template('main/seleccionar_bufete.html', title='Seleccionar Bufete', form=form, bufetes=bufetes, selected_bufete_id=selected_bufete_id)