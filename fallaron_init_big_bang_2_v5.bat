@echo off
REM ============================================================
REM  Archivo: init_big_bang_2_v5.bat
REM  Fecha de creación: 29/07/25
REM  Autor: Giancarlo F. + Tars-90
REM  Motivo: Reinicialización total de la base de datos (Big Bang 2)
REM ============================================================

SET PG_USER=postgres
SET PG_PORT=5432
SET PG_HOST=localhost
SET PG_DB_NAME=software_notarios_dev
SET LOG_DIR="C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask"

echo 🚀 Inicializador Big Bang 2 v5 — Software Notarios
echo ⚠️  Este proceso eliminará y recreará TODA la base de datos de desarrollo.
set /p CONFIRM="¿Estás seguro que deseas continuar? (s/n): "

REM --- Tracking inicial
echo [TRACK] Respuesta inicial: "%CONFIRM%"
echo [TRACK] ASCII de primer caracter: 
for /f %%A in ('cmd /u /c "echo|set /p=%CONFIRM%"') do echo %%A

if /I "%CONFIRM%" NEQ "s" if /I "%CONFIRM%" NEQ "S" (
    echo ❌ Operador canceló el proceso
    goto :eof
)

REM --- PASO 1: Limpieza de migraciones ---
echo.
echo --- PASO 1: Limpieza de migraciones ---
if exist migrations\versions (
    echo 🗑️  Eliminando migraciones previas...
    del /Q migrations\versions\*.*
    echo ✅ Migraciones limpiadas
) else (
    echo ℹ️  Carpeta migrations/versions no existe o ya está vacía
)

REM --- PASO 2: Verificación y creación de base de datos ---
echo.
echo --- PASO 2: Creación de base de datos UTF8 con template0 ---

REM Comprobar si existe la DB
for /f %%i in ('psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -tAc "SELECT 1 FROM pg_database WHERE datname='%PG_DB_NAME%';"') do set DB_EXISTS=%%i

if "%DB_EXISTS%"=="1" (
    echo La base de datos %PG_DB_NAME% EXISTE.
    set /p DROPDB="¿Deseas eliminarla y recrearla? (s/n): "
    echo [TRACK] Respuesta DROPDB: "%DROPDB%"
    echo [TRACK] ASCII de primer caracter DROPDB: 
    for /f %%A in ('cmd /u /c "echo|set /p=%DROPDB%"') do echo %%A

    if /I "%DROPDB%" NEQ "s" if /I "%DROPDB%" NEQ "S" (
        echo ❌ Operador canceló el borrado. Proceso abortado.
        goto :eof
    )

    echo Eliminando base existente...
    psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "DROP DATABASE %PG_DB_NAME%;" postgres 2> %LOG_DIR%\drop.log
    if %errorlevel% neq 0 (
        echo ❌ ERROR al eliminar DB. Revisa drop.log
        goto :eof
    )
)

REM Crear base de datos
psql -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -c "CREATE DATABASE %PG_DB_NAME% WITH ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0 OWNER %PG_USER%;" postgres 2> %LOG_DIR%\create.log
if %errorlevel% neq 0 (
    echo ❌ ERROR al crear DB. Revisa create.log
    goto :eof
)
echo ✅ Base de datos creada correctamente

REM --- PASO 3: Aplicar migraciones ---
echo.
echo --- PASO 3: Aplicando migraciones ---
flask db upgrade 2> %LOG_DIR%\upgrade.log
if %errorlevel% neq 0 (
    echo ❌ ERROR en flask db upgrade. Revisa upgrade.log
    goto :eof
)
echo ✅ Migraciones aplicadas correctamente

REM --- PASO 4: Seed inicial ---
echo.
echo --- PASO 4: Ejecutando seed inicial ---
python -m scripts.seed_inicial 2> %LOG_DIR%\seed.log
if %errorlevel% neq 0 (
    echo ❌ ERROR durante seed inicial. Revisa seed.log
    goto :eof
)
echo ✅ Seed inicial completado

REM --- Éxito final ---
echo.
echo 🎉 Big Bang 2 v5 completado correctamente
pause
