# Navbar SuperAdmin con iconos

## Qué incluye
- `app/templates/partials/_navbar_superadmin.html` — items ordenados, iconos y estado activo por ruta
- `app/static/css/theme_navbar_addon.css` — mejora de espaciado/legibilidad del navbar
- `scripts/patch_navbar_assets.py` — inserta en `base.html` el CDN de Bootstrap Icons y el link al CSS addon

## Cómo aplicar
1. Descomprime en la **raíz** del proyecto (acepta sobrescribir si te pregunta el parcial).
2. Ejecuta:
   ```bat
   python scripts\patch_navbar_assets.py
   ```
3. Reinicia la app y verifica el navbar del SuperAdmin con iconos y mejor espaciado.
