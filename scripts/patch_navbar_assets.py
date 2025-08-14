# archivo: scripts/patch_navbar_assets.py
# última actualización: 2025-08-14 01:31
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-
"""
Inserta en app/templates/base.html:
  - CDN de Bootstrap Icons (si falta)
  - Link a static/css/theme_navbar_addon.css (si falta)
"""

import os

BASE = os.path.join('app', 'templates', 'base.html')

BI_TAG = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">\n'
ADDON_TAG = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/theme_navbar_addon.css\') }}">\n'

def ensure_in_head(markup: str, to_insert: str) -> str:
    idx = markup.lower().rfind('</head>')
    if idx == -1:
        return markup + '\n' + to_insert
    return markup[:idx] + to_insert + markup[idx:]

def main():
    if not os.path.exists(BASE):
        print('[ERROR] No se encontró', BASE)
        return 1

    with open(BASE, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    if 'bootstrap-icons' not in html:
        html = ensure_in_head(html, BI_TAG)
        print('[OK] Agregado CDN de Bootstrap Icons')
        changed = True
    else:
        print('[INFO] Bootstrap Icons ya estaba presente')

    if "css/theme_navbar_addon.css" not in html:
        html = ensure_in_head(html, ADDON_TAG)
        print('[OK] Agregado link a theme_navbar_addon.css')
        changed = True
    else:
        print('[INFO] Link a theme_navbar_addon.css ya estaba presente')

    if changed:
        backup = BASE + '.bak_navbar'
        with open(backup, 'w', encoding='utf-8') as b:
            b.write(html)
        with open(BASE, 'w', encoding='utf-8') as f:
            f.write(html)
        print('[DONE] base.html actualizado')
    else:
        print('[INFO] No se realizaron cambios')

if __name__ == '__main__':
    raise SystemExit(main())
