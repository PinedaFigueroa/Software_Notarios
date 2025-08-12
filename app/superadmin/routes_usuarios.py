# archivo: app/superadmin/routes_usuarios.py
# fecha de creación: 09 / 08 / 25
# cantidad de lineas originales: 260
# última actualización: 12 / 08 / 25 hora 03:25
# motivo de la actualización: CRUD real de Usuarios (listar/buscar, crear, editar, toggle activo)
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

"""Rutas de gestión de Usuarios para SuperAdmin."""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.utils.roles_required import rol_required
from . import superadmin_bp

from app.core_ext import db

from .forms_usuarios import UsuarioForm

from app.models.usuarios import Usuario
try:
    from app.models.usuarios import RolUsuarioEnum
except Exception:
    RolUsuarioEnum = None

BufeteJuridico = None
try:
    from app.models.usuarios import BufeteJuridico
except Exception:
    try:
        from app.models.bufetes import BufeteJuridico
    except Exception:
        pass

def _apply_user_search(query, q: str):
    if q:
        like = f"%{q}%"
        try:
            query = query.filter(
                (Usuario.nombres.ilike(like)) |
                (Usuario.apellidos.ilike(like)) |
                (Usuario.correo.ilike(like))
            )
        except Exception:
            pass
    return query

@superadmin_bp.route('/superadmin/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios_root():
    q = request.args.get('q', type=str, default='')
    query = Usuario.query.order_by(Usuario.id.asc())
    query = _apply_user_search(query, q)
    usuarios = query.all()
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios, bufete_id=None, q=q)

@superadmin_bp.route('/superadmin/bufetes/<int:bufete_id>/usuarios')
@login_required
@rol_required(['SUPERADMIN'])
def listar_usuarios(bufete_id):
    q = request.args.get('q', type=str, default='')
    query = Usuario.query.filter(Usuario.bufete_id == bufete_id).order_by(Usuario.id.asc())
    query = _apply_user_search(query, q)
    usuarios = query.all()
    return render_template('superadmin/usuarios/listar_usuarios.html', usuarios=usuarios, bufete_id=bufete_id, q=q)

@superadmin_bp.route('/superadmin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def crear_usuario():
    form = UsuarioForm()
    form.refresh_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            rol_value = form.rol.data
            rol_obj = None
            if RolUsuarioEnum:
                try:
                    rol_obj = getattr(RolUsuarioEnum, rol_value)
                except Exception:
                    rol_obj = None
            usuario = Usuario(
                nombres=form.nombres.data.strip(),
                apellidos=(form.apellidos.data or '').strip(),
                correo=(form.correo.data or '').strip() or None,
                rol=rol_obj if rol_obj else rol_value,
                bufete_id=int(form.bufete_id.data) if form.bufete_id.data else None,
                activo=bool(form.activo.data),
            )
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('superadmin_bp.listar_usuarios_root'))
        else:
            flash('Por favor corrige los errores del formulario.', 'danger')
    return render_template('superadmin/usuarios/form_usuario.html', titulo='Crear Usuario', form=form)

@superadmin_bp.route('/superadmin/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
@rol_required(['SUPERADMIN'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario)
    form.refresh_choices()
    if request.method == 'POST':
        if form.validate_on_submit():
            rol_value = form.rol.data
            rol_obj = None
            if RolUsuarioEnum:
                try:
                    rol_obj = getattr(RolUsuarioEnum, rol_value)
                except Exception:
                    rol_obj = None
            usuario.nombres = form.nombres.data.strip()
            usuario.apellidos = (form.apellidos.data or '').strip()
            usuario.correo = (form.correo.data or '').strip() or None
            usuario.rol = rol_obj if rol_obj else rol_value
            usuario.bufete_id = int(form.bufete_id.data) if form.bufete_id.data else None
            usuario.activo = bool(form.activo.data)
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('superadmin_bp.listar_usuarios_root'))
        else:
            flash('Por favor corrige los errores del formulario.', 'danger')
    form.rol.data = usuario.rol.name if hasattr(usuario.rol, 'name') else str(usuario.rol)
    form.bufete_id.data = str(usuario.bufete_id) if usuario.bufete_id else ''
    return render_template('superadmin/usuarios/form_usuario.html', titulo=f'Editar: {usuario.nombres}', form=form, usuario=usuario)

@superadmin_bp.route('/superadmin/usuarios/<int:usuario_id>/toggle', methods=['POST'])
@login_required
@rol_required(['SUPERADMIN'])
def toggle_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.activo = not bool(usuario.activo)
    db.session.add(usuario)
    db.session.commit()
    flash(f"Usuario '{usuario.nombres}' ahora está {'activo' if usuario.activo else 'inactivo'}.", 'success')
    next_url = request.args.get('next') or url_for('superadmin_bp.listar_usuarios_root')
    return redirect(next_url)
