# archivo: app/superadmin/routes_usuarios.py
# fecha de creación: 13/08/25
# cantidad de lineas originales: ____
# última actualización: 13/08/25 hora 00:09
# motivo de la actualización: CRUD Usuarios alineado: enums y borrado lógico en borrado_logico
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.security import generate_password_hash
from . import superadmin
from .forms_usuarios import UsuarioForm

# db import robusto
try:
    from app.models.core import db
except Exception:
    try:
        from app.core_ext import db
    except Exception:
        db = None

try:
    from app.models.usuarios import Usuario
    from app.models.bufetes import BufeteJuridico
    from app.models.enums import RolUsuarioEnum
except Exception:
    Usuario = None
    BufeteJuridico = None
    RolUsuarioEnum = None

def _choices_bufetes():
    if not BufeteJuridico:
        return []
    return [(b.id, b.nombre_bufete) for b in BufeteJuridico.query.filter_by(activo=True).all()]

def _choices_roles():
    if not RolUsuarioEnum:
        return []
    # Usamos NAMES como 'SUPERADMIN', 'NOTARIO'...
    return [(m.name, m.value) for m in RolUsuarioEnum]

@superadmin.route('/superadmin/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.filter_by(borrado_logico=False).all() if Usuario else []
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios)

@superadmin.route('/superadmin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    form = UsuarioForm()
    form.bufete_id.choices = _choices_bufetes()
    form.rol.choices = _choices_roles()
    if form.validate_on_submit() and Usuario and db:
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Ya existe un usuario con ese username.', 'warning')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='crear')
        u = Usuario(
            username=form.username.data,
            correo=form.correo.data or None,
            rol=RolUsuarioEnum[form.rol.data] if RolUsuarioEnum else form.rol.data,
            bufete_id=form.bufete_id.data,
            borrado_logico=False,
            password_hash=generate_password_hash(form.password.data or 'Cambiar123!')
        )
        db.session.add(u)
        db.session.commit()
        flash('Usuario creado', 'success')
        return redirect(url_for('superadmin.listar_usuarios'))
    return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='crear')

@superadmin.route('/superadmin/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    if not (Usuario and db):
        return redirect(url_for('superadmin.listar_usuarios'))
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario)
    form.bufete_id.choices = _choices_bufetes()
    form.rol.choices = _choices_roles()
    # Valor inicial del rol en NAME
    try:
        form.rol.data = usuario.rol.name
    except Exception:
        pass
    if form.validate_on_submit():
        # Validar username único
        existe = Usuario.query.filter(Usuario.id != usuario.id, Usuario.username == form.username.data).first()
        if existe:
            flash('Ese username ya está en uso por otro usuario.', 'warning')
            return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)
        usuario.username = form.username.data
        usuario.correo = form.correo.data or None
        usuario.rol = RolUsuarioEnum[form.rol.data] if RolUsuarioEnum else form.rol.data
        usuario.bufete_id = form.bufete_id.data
        # Cambiar password si se envía
        if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('superadmin.listar_usuarios'))
    return render_template('superadmin/usuarios/form_usuario.html', form=form, modo='editar', usuario=usuario)

@superadmin.route('/superadmin/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(usuario_id):
    if not (Usuario and db):
        return redirect(url_for('superadmin.listar_usuarios'))
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.borrado_logico = True
    db.session.commit()
    flash('Usuario eliminado (lógico)', 'warning')
    return redirect(url_for('superadmin.listar_usuarios'))
