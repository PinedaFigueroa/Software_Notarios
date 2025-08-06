@echo off
REM ========================================
REM Generación de Diagrama ER a Colores (Debug)
REM Proyecto: Software Notarios
REM Autor: Giancarlo + Tars-90
REM ========================================

chcp 65001 >NUL
set PYTHONUTF8=1

cd /d %~dp0

echo ==========================================
echo  Generando diagrama ER en colores (DEBUG)
echo ==========================================

set LOG=db_docs\log_colores_debug.txt
mkdir db_docs 2>NUL
mkdir db_docs\Diagramas 2>NUL

python scripts\gen_diagrama_colores_advanced.py > %LOG% 2>&1

echo ==========================================
echo  Proceso finalizado. Revisa:
echo    1) Diagrama en db_docs\Diagramas\
echo    2) Log en %LOG%
echo ==========================================
pause
