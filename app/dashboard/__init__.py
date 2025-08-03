# archivo: app/dashboard/__init__.py
# -*- coding: utf-8 -*-
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from . import routes  # noqa
