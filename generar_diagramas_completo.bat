@echo off
REM =====================================================
REM Software Notarios - Generación Documentación DB
REM Autor: Giancarlo + Tars-90
REM Última actualización: 05/08/2025 18:30
REM =====================================================

cd /d "%~dp0"

set "DOCS_DIR=db_docs"
set "LOG_FILE=%DOCS_DIR%\log_diagramas.txt"
set FECHA=%date% %time%

echo ========================================== > "%LOG_FILE%"
echo  Software Notarios - Generación Documentación DB >> "%LOG_FILE%"
echo  Fecha: %FECHA% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

echo ==========================================
echo 1️⃣ Generando Excel con tablas y columnas...
echo ==========================================
python scripts\gen_db_docs.py >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto end_error

REM =====================================================
REM 2️⃣ Generar diagrama simple
REM =====================================================
echo ==========================================
echo 2️⃣ Generando diagrama ER simple...
echo ==========================================
python scripts\gen_diagrama_simple.py >> "%LOG_FILE%" 2>&1

set "FOUND_FILE="
for %%F in ("%DOCS_DIR%\Diagramas\ERD_SIMPLE_*.png") do set "FOUND_FILE=%%~nxF"

if "%FOUND_FILE%"=="" (
    echo ❌ No se generó diagrama simple >> "%LOG_FILE%"
    goto end_error
)

REM =====================================================
REM 3️⃣ Generar diagrama a color
REM =====================================================
echo ==========================================
echo 3️⃣ Generando diagrama ER a colores...
echo ==========================================
python scripts\gen_diagrama_color.py >> "%LOG_FILE%" 2>&1

set "FOUND_FILE="
for %%F in ("%DOCS_DIR%\Diagramas\ERD_COLOR_*.png") do set "FOUND_FILE=%%~nxF"

if "%FOUND_FILE%"=="" (
    echo ❌ No se generó diagrama a color >> "%LOG_FILE%"
    goto end_error
)

REM =====================================================
REM 4️⃣ Generar PDF multipágina en blanco y negro
REM =====================================================
echo ==========================================
echo 4️⃣ Generando multipágina BW...
echo ==========================================
python scripts\gen_diagrama_multipage_bw.py >> "%LOG_FILE%" 2>&1

set "FOUND_FILE="
for %%F in ("%DOCS_DIR%\Diagramas\ERD_MULTIPAGE_BW_*.pdf") do set "FOUND_FILE=%%~nxF"

if "%FOUND_FILE%"=="" (
    echo ❌ No se generó multipágina BW >> "%LOG_FILE%"
    goto end_error
)

REM =====================================================
REM 5️⃣ Generar PDF multipágina en color
REM =====================================================
echo ==========================================
echo 5️⃣ Generando multipágina color...
echo ==========================================
python scripts\gen_diagrama_multipage_color.py >> "%LOG_FILE%" 2>&1

set "FOUND_FILE="
for %%F in ("%DOCS_DIR%\Diagramas\ERD_MULTIPAGE_COLOR_*.pdf") do set "FOUND_FILE=%%~nxF"

if "%FOUND_FILE%"=="" (
    echo ❌ No se generó multipágina color >> "%LOG_FILE%"
    goto end_error
)

echo ==========================================
echo ✅ Proceso completado con éxito
echo Documentación generada en %DOCS_DIR%
echo Log detallado: %LOG_FILE%
echo ==========================================
pause
exit /b 0

:end_error
echo ==========================================
echo ❌ Proceso finalizado con errores
echo Revisa el log: %LOG_FILE%
echo ==========================================
pause
exit /b 1
