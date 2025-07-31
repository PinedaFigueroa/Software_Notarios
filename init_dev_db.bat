@echo off
REM ==========================================================================
REM 🎉 init_dev_db.bat — Inicializa la base de datos software_notarios en UTF8
REM Crea migraciones iniciales, aplica y ejecuta seed inicial.
REM Fecha creación: 14/07/25
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

echo.
echo ======================================================================
echo       🚀 INICIALIZADOR DE BASE DE DATOS Y SEED INICIAL (DEV)
echo ======================================================================
echo.
echo ⚠ ADVERTENCIA: Este script ELIMINARÁ y RECREARÁ la base de datos "%PG_DB_NAME%"
echo TODOS los datos existentes se perderán.
echo.
set /p CONFIRM="¿Desea continuar? (s/N): "
if /i "%CONFIRM%" neq "s" (
    echo ❌ Operación cancelada.
    goto :eof
)

REM 📦 Forzar UTF-8
chcp 65001 >NUL
set PYTHONIOENCODING=utf-8

REM Configure FLASK_APP para app factory
set FLASK_APP=app:create_app

echo.
echo --- 🔄 PASO 1: Eliminando base de datos "%PG_DB_NAME%" (si existe) ---
set PGPASSWORD=%PG_PASSWORD%
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "DROP DATABASE IF EXISTS %PG_DB_NAME%;" postgres 2> %LOG_DIR%\drop.log
if %errorlevel% neq 0 (
    echo ❌ ERROR al eliminar DB. Revisa %LOG_DIR%\drop.log
    goto :eof
)
REM echo ✅ Base de datos eliminada.
echo ✅ Base de datos "%PG_DB_NAME%" eliminada.

echo.
echo --- 🛠 PASO 2: Creando base de datos "%PG_DB_NAME%" con UTF8 ---
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "CREATE DATABASE %PG_DB_NAME% WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER %PG_USER%;" postgres 2> %LOG_DIR%\create.log
if %errorlevel% neq 0 (
    echo ❌ ERROR al crear DB. Revisa %LOG_DIR%\create.log
    goto :eof
)
REM echo ✅ Base de datos creada.
echo ✅ Base de datos "%PG_DB_NAME%" creada.

echo.
echo --- ⚙ PASO 3: Inicializando Flask-Migrate (Alembic) ---
rmdir /s /q migrations 2>nul
python -m flask db init 2> %LOG_DIR%\init.log
if %errorlevel% neq 0 (
    echo ❌ ERROR flask db init. Revisa %LOG_DIR%\init.log
    goto :eof
)
echo ✅ Flask-Migrate inicializado.

echo.
echo --- 📦 PASO 4: Generando migración inicial ---
python -m flask db migrate -m "Big Bang: Initial creation" 2> %LOG_DIR%\migrate.log
if %errorlevel% neq 0 (
    echo ❌ ERROR flask db migrate. Revisa %LOG_DIR%\migrate.log
    goto :eof
)
echo ✅ Migración generada.

echo.
echo --- 🏗 PASO 5: Aplicando migración ---
python -m flask db upgrade 2> %LOG_DIR%\upgrade.log
if %errorlevel% neq 0 (
    echo ❌ ERROR flask db upgrade. Revisa %LOG_DIR%\upgrade.log
    goto :eof
)
echo ✅ Migración aplicada.

echo.
echo --- 🌱 PASO 6: Ejecutando seed inicial ---
python -m flask seed-cli init 2> %LOG_DIR%\seedcli.log
if %errorlevel% neq 0 (
    echo ❌ ERROR seed-cli. Revisa %LOG_DIR%\seedcli.log
    goto :eof
)
echo ✅ Seed inicial completado.

echo.
echo ✅✅✅ COMPLETADO: DB, migraciones y seed creados con éxito.
echo.
endlocal
pause
