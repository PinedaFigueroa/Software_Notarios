@echo off
:: archivo: git_commit_limpio.bat
:: fecha de creación: 2025-08-07
:: hora: 02:55
:: autor: Giancarlo + Tars-90
:: -*- coding: utf-8 -*-

echo ==================================================
echo   🚀 COMMIT LIMPIO - Software Notarios
echo ==================================================
echo.

:: Evitar archivos .pyc y __pycache__
echo 🧼 Limpiando archivos no deseados del stage...
git reset app/__pycache__/cli.*.pyc > nul 2>&1
git reset app/models/__pycache__/*.pyc > nul 2>&1

:: Agregar cambios importantes
echo ➕ Agregando archivos clave...
git add app/cli.py
git add app/models/bufetes.py
git add app/models/core.py
git add app/models/usuarios.py
git add init_dev_db.bat
git add migrations/versions/
git add scripts/
git add db_docs/

:: Confirmación
echo.
echo ✅ Archivos añadidos. Realizando commit...

git commit -m "🌱 Commit limpio 2025-08-07 02:55 - Seed, modelos corregidos, scripts y migración"

echo.
echo ☁ Haciendo push a origin/main...
git push origin main

echo.
echo ✅ Proceso completado con éxito.
pause
