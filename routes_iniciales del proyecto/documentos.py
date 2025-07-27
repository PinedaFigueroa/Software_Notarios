# C:\Users\Usuario\Mi unidad\Notarios_app\app\routes\documentos.py
# Última Actualización: 2025-07-08 20:55:00 (GMT-6, Hora de Guatemala)
# Motivo de la Actualización: Adaptado a modelos mínimos.
#                              Comentadas importaciones de modelos no esenciales para permitir el inicio.
# Desarrollador: Gemini (con la dirección de Giancarlo F.)

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

# Importar solo los modelos que están en core_models.py
from ..models.core_models import db, UsuarioSistema, BufeteJuridico, Notario # <--- Solo modelos esenciales
# Importar ENUMs necesarios
from ..models.enums import RolUsuarioSistema 

# Importar formularios necesarios (ninguno de documentos en la versión mínima)
# from app.forms import DocumentoNotarialForm, EscrituraPublicaForm, ActaNotarialForm, AvisoForm

# Importar el procesador de contexto para acceder a la info del bufete activo
from app.context_processors import get_bufete_info

# Importar decorador de roles
from app.decorators import role_required

log = logging.getLogger(__name__)

documentos_bp = Blueprint('documentos_bp', __name__)

# --- Rutas de Documentos Notariales (Solo Listado Básico por ahora) ---
@documentos_bp.route('/')
@documentos_bp.route('/listado')
@login_required
def listado_documentos():
    flash('La gestión de documentos notariales está en desarrollo. Solo se muestra un placeholder.', 'info')
    return render_template('documentos/listado_documentos.html', title='Gestión de Documentos Notariales', documentos=[])

# Las rutas de agregar/editar/eliminar documentos se implementarán en fases posteriores
# @documentos_bp.route('/agregar_escritura_publica', methods=['GET', 'POST'])
# @login_required
# @role_required(RolUsuarioSistema.NOTARIO.value, RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
# def agregar_escritura_publica():
#     flash('La función de agregar escritura pública está en desarrollo.', 'info')
#     return redirect(url_for('documentos_bp.listado_documentos'))

# @documentos_bp.route('/editar_escritura_publica/<int:documento_id>', methods=['GET', 'POST'])
# @login_required
# @role_required(RolUsuarioSistema.NOTARIO.value, RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
# def editar_escritura_publica(documento_id):
#     flash('La función de editar escritura pública está en desarrollo.', 'info')
#     return redirect(url_for('documentos_bp.listado_documentos'))

# @documentos_bp.route('/eliminar_documento/<int:documento_id>', methods=['POST'])
# @login_required
# @role_required(RolUsuarioSistema.SUPER_ADMINISTRADOR.value, RolUsuarioSistema.ADMINISTRADOR.value)
# def eliminar_documento(documento_id):
#     flash('La función de eliminar documento está en desarrollo.', 'info')
#     return redirect(url_for('documentos_bp.listado_documentos'))
