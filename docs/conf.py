# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Software para Notarios'
copyright = '2025, Giancarlo E. Figueroa F. / HUBSA'
author = 'Giancarlo E. Figueroa F.'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',       # extraer docstrings de los módulos Python
    'sphinx.ext.napoleon',      # soportar Google y NumPy style docstrings
    'sphinx.ext.viewcode',      # añadir enlaces al código fuente
     'myst_parser',  # ⬅ Permite usar archivos .md
     'docxbuilder',             # ⬅ Para exportar a .docx

]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'   # Tema Read The Docs (muy usado)
html_static_path = ['_static']

# -- Autodoc settings (opcional, para más control) --------------------------
autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = True
