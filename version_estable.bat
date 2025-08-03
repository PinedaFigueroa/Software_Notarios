@echo off
REM ==========================================================================
REM 🚀 restore_stable_e4fe265.bat — Recupera la versión estable con Dashboard
REM Commit: e4fe265 (🎨 Dashboard funcionando con Bootstrap local, navbar azul)
REM Autor: Giancarlo + Tars‑90
REM ==========================================================================

setlocal

REM 🐘 Configuración DB
set PG_USER=postgres
set PG_PASSWORD=12345678
set PG_HOST=localhost
set PG_PORT=5432
set PG_DB_NAME=software_notarios

REM 📂 Carpeta de logs de error
set LOG_DIR="%~dp0errores_bdd_flask"
mkdir %LOG_DIR% >NUL 2>&1

chcp 65001 >NUL
set PYTHONIOENCODING=utf-8

echo.
echo =============================================================
echo       🚀 RECUPERANDO VERSION ESTABLE e4fe265

echo Paso 1️⃣: Guardar cambios actuales (commit temporal)
git add .
git commit -m "⏳ WIP: backup temporal antes de restaurar e4fe265" --allow-empty

if %errorlevel% neq 0 (
    echo ❌ ERROR creando commit temporal
    pause
    goto :eof
)

echo.
echo Paso 2️⃣: Crear rama temporal stable/recovery_0208
 git checkout -b stable/recovery_0208

REM Recuperar commit estable e4fe265
echo.
echo Paso 3️⃣: Resetear a commit estable e4fe265
 git reset --hard e4fe265

REM Limpiar pycache y reinstalar dependencias
echo.
echo Paso 4️⃣: Limpiando __pycache__ y reinstalando dependencias
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
pip install -r requirements.txt

REM Borrar DB y recrear
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "DROP DATABASE IF EXISTS %PG_DB_NAME%;" postgres
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "CREATE DATABASE %PG_DB_NAME% WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER %PG_USER%;" postgres

REM Migrar y seed inicial
echo.
echo Paso 5️⃣: Migraciones y seed inicial
set FLASK_APP=app:create_app
flask db upgrade
flask seed-cli init

echo.
echo ✅ Listo. Ahora puedes ejecutar:
echo flask run

echo =============================================================
pause
