# README corrige referencias legacy a endpoints del SuperAdmi
# Endpoint Fix Kit
Fecha: 13/08/25 hora 00:52

Este kit corrige referencias legacy a endpoints del SuperAdmin (por ejemplo `superadmin_bp.listar_usuarios_root`) y las reemplaza por los canónicos `superadmin.*`.

## Uso
1. Copia la carpeta `scripts/` en la **raíz** de tu proyecto.
2. Ejecuta **PowerShell**:
   ```powershell
   .\scripts\fix_endpoints.ps1 -Root .
   ```
   o simplemente corre el wrapper:
   ```bat
   scripts\fix_endpoints.bat
   ```
3. Revisa el resumen de coincidencias restantes. Si aún quedan líneas, compárteme el path y lo corregimos.

## Qué reemplaza
- `superadmin_bp.listar_usuarios_root` → `superadmin.listar_usuarios`
- `superadmin_bp.listar_usuarios` → `superadmin.listar_usuarios`
- `superadmin_bp.crear_usuarios` → `superadmin.crear_usuario`
- `superadmin_bp.editar_usuarios` → `superadmin.editar_usuario`
- `superadmin_bp.eliminar_usuarios` → `superadmin.eliminar_usuario`
- `superadmin.listar_usuarios_root` → `superadmin.listar_usuarios`
- `superadmin_bp.dashboard_global` → `superadmin.dashboard_global`
- Equivalentes de bufetes.

Tras ejecutar, valida con:
```
flask routes
```
y prueba `/superadmin/dashboard`.
