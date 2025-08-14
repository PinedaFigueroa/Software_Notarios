# archivo: app/superadmin/routes_usuarios.py
# última actualización: 13/08/25 hora 02:39
# autor: Giancarlo + Tars-90
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import superadmin_bp
from .forms_usuarios import UsuarioForm

try:
    from app.models.core import db
except Exception:
    from app.core_ext import db

from app.models.usuarios import Usuario
from app.models.bufetes import BufeteJuridico
from app.models.enums import RolUsuarioEnum

def _choices_bufetes():
    return [(b.id, b.nombre_bufete) for b in BufeteJuridico.query.filter_by(activo=True).all()]

def _choices_roles():
    return [(m.name, m.value) for m in RolUsuarioEnum if m.name != 'SUPERADMIN']

def _admins_count(bufete_id, exclude_user_id=None):
    q = Usuario.query.filter_by(bufete_id=bufete_id, borrado_logico=False)
    q = q.filter(Usuario.rol == RolUsuarioEnum.ADMINISTRADOR)
    if exclude_user_id:
        q = q.filter(Usuario.id != exclude_user_id)
    return q.count()

@superadmin_bp.route('/superadmin/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.filter_by(borrado_logico=False).all()
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios)

@superadmin_bp.route('/superadmin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    form = UsuarioForm()
    form.bufete_id.choices = _choices_bufetes()
    form.rol.choices = _choices_roles()
    if form.validate_on_submit():
        if form.rol.data == 'SUPERADMIN':
            flash('Creación de SUPERADMIN vía UI no permitida.', 'danger')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='crear')
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Ya existe un usuario con ese username.', 'warning')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='crear')
        u = Usuario(
            username=form.username.data,
            correo=form.correo.data or None,
            rol=RolUsuarioEnum[form.rol.data],
            bufete_id=form.bufete_id.data,
            borrado_logico=False,
            password_hash=generate_password_hash(form.password.data or 'Cambiar123!')
        )
        db.session.add(u)
        db.session.commit()
        flash('Usuario creado', 'success')
        return redirect(url_for('superadmin.listar_usuarios'))
    return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='crear')

@superadmin_bp.route('/superadmin/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario)
    form.bufete_id.choices = _choices_bufetes()
    form.rol.choices = _choices_roles()
    try:
        form.rol.data = usuario.rol.name
    except Exception:
        pass
    if form.validate_on_submit():
        if form.rol.data == 'SUPERADMIN':
            flash('Asignación de SUPERADMIN vía UI no permitida.', 'danger')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)
        if usuario.rol == RolUsuarioEnum.ADMINISTRADOR:
            if (form.rol.data != 'ADMINISTRADOR') or (form.bufete_id.data != usuario.bufete_id):
                if _admins_count(usuario.bufete_id, exclude_user_id=usuario.id) == 0:
                    flash('Este cambio dejaría al bufete sin administrador.', 'warning')
                    return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)
        existe = Usuario.query.filter(Usuario.id != usuario.id, Usuario.username == form.username.data).first()
        if existe:
            flash('Ese username ya está en uso por otro usuario.', 'warning')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)
        usuario.username = form.username.data
        usuario.correo = form.correo.data or None
        usuario.rol = RolUsuarioEnum[form.rol.data]
        usuario.bufete_id = form.bufete_id.data
        if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('superadmin.listar_usuarios'))
    return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)

@superadmin_bp.route('/superadmin/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.rol == RolUsuarioEnum.ADMINISTRADOR and _admins_count(usuario.bufete_id, exclude_user_id=usuario.id) == 0:
        flash('No puedes eliminar al único administrador del bufete.', 'warning')
        return redirect(url_for('superadmin.listar_usuarios'))
    usuario.borrado_logico = True
    db.session.commit()
    flash('Usuario eliminado (lógico)', 'warning')
    return redirect(url_for('superadmin.listar_usuarios'))
