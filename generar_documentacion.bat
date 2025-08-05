@echo off
REM =====================================================
REM  generar_documentacion_db.bat
REM  Autor: Giancarlo + Tars-90
REM  Fecha: 03/08/25
REM  Descripción:
REM    Ejecuta todos los scripts de documentación, exportación
REM    y generación de diagramas de la BDD del proyecto.
REM =====================================================

echo ==========================================
echo  Software Notarios - Generación Documentación DB
echo ==========================================

REM Activar entorno virtual
call swnot\Scripts\activate

REM Crear carpeta de documentación si no existe
if not exist db_docs mkdir db_docs

REM Limpiar generación anterior
echo Limpiando db_docs anterior...
del /q db_docs\*.*
echo.

REM 1. Exportar tablas a Excel con colores
echo Exportando tablas a Excel...
python scripts\export_tablas_excel.py

REM 2. Exportar estructura de DB a PDF
echo Exportando estructura DB a PDF...
python scripts\export_db_pdf.py

REM 3. Generar diagrama ERAlchemy (png)
echo Generando diagrama ERAlchemy...
python scripts\generar_diagrama_eralchemy.py

REM 4. Generar diagrama coloreado
echo Generando diagrama coloreado por roles/entidades...
python scripts\generar_diagrama_colores.py

REM 5. Generar diagramas por páginas
echo Generando diagramas por páginas para impresión...
python scripts\generar_diagrama_paginas.py

REM 6. Backup de diagramas
echo Realizando backup de diagramas...
python scripts\backup_diagramas.py

echo.
echo ==========================================
echo  DOCUMENTACIÓN COMPLETA GENERADA EN db_docs
echo ==========================================

pause
