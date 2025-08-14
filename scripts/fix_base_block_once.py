# archivo: scripts/fix_base_block_once.py
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-
import os, re

TARGET = os.path.join('app', 'templates', 'base.html')
GOOD   = "{% block content %}{% endblock %}"

if not os.path.exists(TARGET):
    print("[ERROR] No se encontró", TARGET)
    raise SystemExit(1)

with open(TARGET, 'r', encoding='utf-8') as f:
    txt = f.read()

patterns = [
    re.compile(r"\{\%\s*block\s+content\s*\%\}\s*\}\s*\{\%\s*endblock\s*\%\}"),
    re.compile(r"\{\%\s*block\s+content\s*\%\}\s*\}\s*$", re.M),
]

count = 0
for rx in patterns:
    txt, n = rx.subn(GOOD, txt)
    count += n

if count:
    with open(TARGET + '.bak_basefix', 'w', encoding='utf-8') as b:
        b.write(open(TARGET, 'r', encoding='utf-8').read())
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(txt)
    print(f"[OK] Corregido base.html (+{count} reemplazo/s)")
else:
    print("[INFO] No se detectó el patrón defectuoso. Revisa la línea con 'block content' manualmente.")
