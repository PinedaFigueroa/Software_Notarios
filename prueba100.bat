@echo off
chcp 65001 >nul

REM ========================================
REM Script: prueba100.bat
REM Proyecto: Software Notarios
REM Autor: Giancarlo F. + Tars-90
REM ========================================

REM --- Ruta base del proyecto ---
set BASEDIR=%~dp0..
set LOGFILE="%BASEDIR%\db_docs\log_prueba100.txt"

REM --- Crear carpetas ---
if not exist "%BASEDIR%\db_docs" mkdir "%BASEDIR%\db_docs"
if not exist "%BASEDIR%\db_docs\Listados" mkdir "%BASEDIR%\db_docs\Listados"
if not exist "%BASEDIR%\db_docs\Diagramas" mkdir "%BASEDIR%\db_docs\Diagramas"

echo ========================================== 
echo  Software Notarios - Generacion Documentacion DB
echo ==========================================
echo Log creado en: %LOGFILE%

REM --- PASO 1: Generar Excel ---
echo Generando Excel con tablas y columnas...
python "%BASEDIR%\scripts\gen_db_docs.py" >> %LOGFILE% 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR en gen_db_docs.py (ver log)
    goto END
) else (
    echo Excel generado correctamente
)

REM --- PASO 2: Generar diagrama coloreado ---
echo Generando diagrama ER a color...
python "%BASEDIR%\scripts\gen_diagrama_color.py" >> %LOGFILE% 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR en gen_diagrama_color.py (ver log)
    goto END
) else (
    echo Diagramas ER generados
)

REM --- PASO 3: Generar PDF multipagina ---
echo Generando PDF multipagina 4x4...
python "%BASEDIR%\scripts\gen_diagrama_multipage.py" >> %LOGFILE% 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR en gen_diagrama_multipage.py (ver log)
    goto END
) else (
    echo PDF multipagina generado
)

:END
echo ==========================================
echo Proceso finalizado. Revisa la carpeta db_docs
echo Log detallado: %LOGFILE%
echo ==========================================
pause
