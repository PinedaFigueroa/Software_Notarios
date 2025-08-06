@echo off
REM ========================================
REM Generación de Documentación y Diagramas BDD
REM Proyecto: Software Notarios
REM Autor: Giancarlo + Tars-90
REM ========================================

chcp 65001 >nul

REM Cambiar al directorio raíz del proyecto
cd /d %~dp0

REM Crear fecha y hora seguras
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set FECHA=%%c%%b%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set HORA=%%a%%b

REM Crear carpetas si no existen
if not exist db_docs mkdir db_docs
if not exist db_docs\Listados mkdir db_docs\Listados
if not exist db_docs\Diagramas mkdir db_docs\Diagramas
if not exist logs mkdir logs

set LOG=logs\log_%FECHA%_%HORA%.txt

echo ==========================================
echo   Software Notarios - Generación Documentación DB
echo ==========================================
echo Log: %LOG%
echo ==========================================

echo [1/3] Exportando tablas y columnas a Excel...
python scripts\gen_db_docs.py >> %LOG% 2>&1

echo [2/3] Generando diagramas ER (PNG y PDF)...
python scripts\gen_diagrama_color.py >> %LOG% 2>&1

echo [3/3] Generando diagrama multipágina 4x4...
python scripts\gen_diagrama_multipage.py >> %LOG% 2>&1

echo ==========================================
echo   DOCUMENTACIÓN COMPLETA GENERADA EN db_docs
echo   Revisa el log: %LOG%
echo ==========================================
pause
