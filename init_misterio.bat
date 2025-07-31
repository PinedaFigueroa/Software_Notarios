@echo off
REM ============================================================
REM  Archivo: init_misterio.bat (Big Bang 2 v8)
REM  Fecha: 29/07/25
REM  Autor: Giancarlo F. + Tars-90
REM  Motivo: Reinicialización total de DB con limpieza forzada
REM ============================================================

SET PG_USER=postgres
SET PG_PORT=5432
SET PG_HOST=localhost
SET PG_DB_NAME=software_notarios_dev
SET LOG_DIR="C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask"

echo ===========================================================
echo       INICIALIZADOR DE BASE DE DATOS Y SEED INICIAL
echo ===========================================================
echo.
echo ADVERTENCIA: Este script ELIMINARÁ y RECREARÁ la base "%PG_DB_NAME%"
echo TODOS los datos existentes se perderán.
echo.
set /p CONFIRM="Desea continuar? (s/N): "

echo [TRACK] Respuesta inicial: "%CONFIRM%" > %LOG_DIR%\init_misterio.log

if /I "%CONFIRM%" NEQ "s" if /I "%CONFIRM%" NEQ "S" (
    echo ❌ Operador canceló el proceso
    echo [LOG] Operador canceló en la primera confirmación >> %LOG_DIR%\init_misterio.log
    goto :eof
)

echo.
echo --- 🔄 PASO 1: Eliminando base de datos "%PG_DB_NAME%" (FORCE) ---
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "DROP DATABASE IF EXISTS %PG_DB_NAME% WITH (FORCE);" postgres 2>> %LOG_DIR%\drop.log
if %errorlevel% neq 0 (
    echo ❌ ERROR al eliminar DB. Revisa drop.log
    goto :eof
)
echo ✅ Base de datos eliminada.
timeout /t 2 >nul

echo.
echo --- 🛠 PASO 2: Creando base de datos "%PG_DB_NAME%" UTF8 ---
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "CREATE DATABASE %PG_DB_NAME% WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER %PG_USER%;" postgres 2>> %LOG_DIR%\create.log
if %errorlevel% neq 0 (
    echo ❌ ERROR al crear DB. Revisa create.log
    goto :eof
)
echo ✅ Base de datos creada.
timeout /t 2 >nul

echo.
echo --- 🔹 PASO 2.5: Limpieza de posibles restos ---
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d %PG_DB_NAME% -c "DROP TABLE IF EXISTS alembic_version;" 2>> %LOG_DIR%\cleanup.log

echo.
echo --- ⚙ PASO 3: Inicializando Flask-Migrate ---
if exist migrations (
    rmdir /s /q migrations
)
flask db init 2>> %LOG_DIR%\db_init.log
if %errorlevel% neq 0 (
    echo ❌ ERROR en flask db init. Revisa db_init.log
    goto :eof
)
echo ✅ Flask-Migrate inicializado.

echo.
echo --- 📦 PASO 4: Generando migración inicial ---
flask db migrate -m "big bang initial creation" 2>> %LOG_DIR%\db_migrate.log
if %errorlevel% neq 0 (
    echo ❌ ERROR en flask db migrate. Revisa db_migrate.log
    goto :eof
)
echo ✅ Migración generada.

echo.
echo --- 🏗 PASO 5: Aplicando migración ---
flask db upgrade 2>> %LOG_DIR%\upgrade.log
if %errorlevel% neq 0 (
    echo ❌ ERROR en flask db upgrade. Revisa upgrade.log
    goto :eof
)
echo ✅ Migración aplicada.

echo.
echo --- 🌱 PASO 6: Ejecutando seed inicial ---
python -m scripts.seed_inicial 2>> %LOG_DIR%\seed.log
if %errorlevel% neq 0 (
    echo ❌ ERROR durante seed inicial. Revisa seed.log
    goto :eof
)
echo ✅ Seed inicial completado.

echo.
echo 🎉✅ COMPLETADO: DB, migraciones y seed creados con éxito.
pause
