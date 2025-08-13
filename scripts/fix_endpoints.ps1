# archivo: scripts\fix_endpoints.ps1
# última actualización: 13/08/25 hora 00:52
# motivo: Reemplazar endpoints legacy a los canónicos del blueprint 'superadmin'
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

param(
  [string]$Root = '.'
)

Write-Host "==> Buscando y reemplazando endpoints legacy en $Root" -ForegroundColor Cyan

$patterns = @{
  'superadmin_bp\.listar_usuarios_root' = 'superadmin.listar_usuarios'
  'superadmin_bp\.listar_usuarios'      = 'superadmin.listar_usuarios'
  'superadmin_bp\.crear_usuarios'       = 'superadmin.crear_usuario'
  'superadmin_bp\.editar_usuarios'      = 'superadmin.editar_usuario'
  'superadmin_bp\.eliminar_usuarios'    = 'superadmin.eliminar_usuario'

  'superadmin\.listar_usuarios_root'    = 'superadmin.listar_usuarios'

  'superadmin_bp\.listar_bufetes'       = 'superadmin.listar_bufetes'
  'superadmin_bp\.crear_bufetes'        = 'superadmin.crear_bufete'
  'superadmin_bp\.editar_bufetes'       = 'superadmin.editar_bufete'
  'superadmin_bp\.eliminar_bufetes'     = 'superadmin.eliminar_bufete'

  'superadmin_bp\.dashboard_global'     = 'superadmin.dashboard_global'
}

$files = Get-ChildItem -Path $Root -Recurse -Include *.py,*.html -File

foreach ($f in $files) {
  $content = Get-Content -Raw -LiteralPath $f.FullName
  $orig = $content
  foreach ($k in $patterns.Keys) {
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, $k, $patterns[$k])
  }
  if ($content -ne $orig) {
    Write-Host "  • Corrigiendo: $($f.FullName)" -ForegroundColor Green
    Set-Content -LiteralPath $f.FullName -Value $content -Encoding UTF8
  }
}

Write-Host "==> Verificación (coincidencias restantes):" -ForegroundColor Yellow
$leftovers = Select-String -Path $Root\**\*.py,$Root\**\*.html -Pattern 'superadmin_bp\.|listar_usuarios_root' -AllMatches -ErrorAction SilentlyContinue
if ($leftovers) {
  $leftovers | ForEach-Object { "$($_.Path):$($_.LineNumber): $($_.Line.Trim())" } | Write-Host
} else {
  Write-Host "  ✓ Sin coincidencias legacy" -ForegroundColor Green
}