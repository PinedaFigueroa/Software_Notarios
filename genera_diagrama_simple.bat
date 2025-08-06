@echo off
REM Generador de diagrama ER limpio y funcional

REM Cambiar al directorio raíz del proyecto
cd /d %~dp0

REM Crear timestamp seguro: YYYYMMDD_HHMM
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set FECHA=%%c%%b%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set HORAS=%%a%%b
set TIMESTAMP=%FECHA%_%HORAS%

REM Crear carpetas
if not exist db_docs mkdir db_docs
if not exist db_docs\Diagramas mkdir db_docs\Diagramas

set OUTPUT=db_docs\Diagramas\ERD_SIMPLE_%TIMESTAMP%.png

echo =============================
echo Generando diagrama con ERAlchemy...
echo =============================

eralchemy -i postgresql+psycopg2://postgresql:12345678@localhost:5432/software_notarios -o "%OUTPUT%"

if exist "%OUTPUT%" (
    echo Diagrama generado correctamente en: %OUTPUT%
) else (
    echo ❌ ERROR: No se generó el diagrama. Revisa la configuración de ERAlchemy o conexión DB.
)

pause
