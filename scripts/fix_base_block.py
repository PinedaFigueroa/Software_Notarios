# -*- coding: utf-8 -*-
# archivo: scripts/fix_base_block.py
# última actualización: 13/08/25 hora 01:21
# autor: Giancarlo + Tars-90
"""
Repara en app/templates/base.html el patrón:
    {% block content %}}{% endblock %}
por el correcto:
    {% block content %}{% endblock %}
Uso:
    python scripts/fix_base_block.py
"""
import os, re

def main():
    base_path = os.path.join('app', 'templates', 'base.html')
    if not os.path.exists(base_path):
        print('[INFO] No se encontró', base_path)
        return
    with open(base_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    new, n = re.subn(r"\{\%\s*block\s+content\s*\%\}\}}\s*\{\%\s*endblock\s*\%\}", "{% block content %}{% endblock %}", txt)
    if n > 0:
        with open(base_path + '.bak_basefix', 'w', encoding='utf-8') as b:
            b.write(txt)
        with open(base_path, 'w', encoding='utf-8') as f:
            f.write(new)
        print('[OK] Corregido base.html (+%d reemplazo/s)' % n)
    else:
        print('[INFO] No se encontró el patrón a corregir en base.html')

if __name__ == '__main__':
    main()
