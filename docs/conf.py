# Configuration file for the Sphinx documentation builder.
# -*- coding: utf-8 -*-
#
# Software Notarios Documentation
# Autor: Giancarlo Figueroa + Tars-90
# Última actualización: 31 / 07 / 25 - 16:00

import os
import sys

# --- Rutas para autodoc ---
# Agregar raíz del proyecto y carpeta app para que Sphinx encuentre los módulos
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../app'))
sys.path.insert(0, os.path.abspath('../scripts'))

# --- Proyecto ---
project = 'Software Notarios'
author = 'Giancarlo Figueroa + Tars-90'
release = '1.0.0'

# --- Extensiones ---
extensions = [
    'sphinx.ext.autodoc',      # Documentación automática de módulos Python
    'sphinx.ext.napoleon',     # Docstrings estilo Google/NumPy
    'sphinx.ext.viewcode',     # Muestra el código fuente con enlaces
    'sphinx.ext.todo',         # Soporte para TODOs
    'sphinx.ext.githubpages',  # Para publicar en GitHub Pages
    'myst_parser'              # Para soportar archivos Markdown
]


# --- Idioma ---
language = 'es'

# --- Plantilla ---
templates_path = ['_templates']

# --- Archivos ignorados ---
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# --- Salida HTML ---
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme' # para mejorar la presentación 
html_static_path = ['_static']

# --- Opciones autodoc ---
autodoc_member_order = 'bysource'
autoclass_content = 'both'
add_module_names = True
