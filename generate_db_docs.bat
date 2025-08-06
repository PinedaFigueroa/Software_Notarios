@echo off
REM ========================================
REM Generación de Documentación y Diagramas BDD
REM Proyecto: Software Notarios
REM Autor: Giancarlo + Tars-90
REM Última actualización: 05/08/2025
REM ========================================

REM Cambiar al directorio del BAT
cd /d %~dp0

REM Crear fecha y hora seguras para nombres de archivo
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set FECHA=%%c%%b%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set HORA=%%a%%b
set TIMESTAMP=%FECHA%_%HORA%

REM Crear carpetas si no existen
if not exist db_docs mkdir db_docs
if not exist db_docs\Listados mkdir db_docs\Listados
if not exist db_docs\Diagramas mkdir db_docs\Diagramas

REM Crear log
set LOG=db_docs\log_%TIMESTAMP%.txt

echo ================================
echo Generando Excel con tablas y columnas...
echo ================================
python scripts\gen_db_listings.py >> %LOG% 2>&1

echo ================================
echo Generando diagramas ER en PNG y PDF a color...
echo ================================
python scripts\gen_db_diagrams.py >> %LOG% 2>&1

echo ================================
echo Generando diagramas multipagina 3x3 y 4x4...
echo ================================
python scripts\gen_db_diagrams_multipage.py 3 3 >> %LOG% 2>&1
python scripts\gen_db_diagrams_multipage.py 4 4 >> %LOG% 2>&1

echo ================================
echo Creando README con fecha y hora
echo ================================
echo Documentación BDD generada el %date% a las %time% > db_docs\README_docs.md

echo ================================
echo Proceso finalizado. 
echo Revisa la carpeta db_docs\ para los resultados
echo ================================
pause
