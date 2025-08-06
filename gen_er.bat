@echo off
REM ============================================
REM Generador de diagrama ER con debug/log
REM Proyecto: Software Notarios
REM Autor: Giancarlo F. + Tars-90
REM Fecha: 05/08/2025
REM ============================================

REM Activar eco y rastreo
setlocal ENABLEDELAYEDEXPANSION
echo [INFO] Iniciando script de generación de diagrama ER...
echo [INFO] Directorio actual: %CD%

REM --- Timestamp seguro ---
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set FECHA=%%c%%b%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set HORAS=%%a%%b
set TIMESTAMP=%FECHA%_%HORAS%

REM --- Crear carpetas si no existen ---
if not exist db_docs (
    echo [INFO] Creando carpeta db_docs
    mkdir db_docs
)
if not exist db_docs\Diagramas (
    echo [INFO] Creando carpeta db_docs\Diagramas
    mkdir db_docs\Diagramas
)

REM --- Archivo de salida y log ---
set OUTPUT=db_docs\Diagramas\ERD_DEBUG_%TIMESTAMP%.png
set LOG=db_docs\debug_%TIMESTAMP%.log

echo [INFO] Archivo de salida: %OUTPUT%
echo [INFO] Log de depuración: %LOG%

REM --- Verificar si eralchemy está en PATH ---
where eralchemy >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ERAlchemy no está en el PATH. >> %LOG%
    echo ❌ ERROR: ERAlchemy no está en el PATH.
    pause
    exit /b
)

REM --- Ejecutar ERAlchemy con rastreo ---
echo [INFO] Ejecutando ERAlchemy... >> %LOG%
echo Comando: eralchemy -i postgresql+psycopg2://default:12345678@localhost:5432/software_notarios -o "%OUTPUT%" >> %LOG%

eralchemy -i postgresql+psycopg2://default:12345678@localhost:5432/software_notarios -o "%OUTPUT%" 1>>%LOG% 2>>&1

REM --- Verificar resultado ---
if exist "%OUTPUT%" (
    echo ✅ Diagrama generado correctamente en: %OUTPUT%
    echo [INFO] Generación exitosa >> %LOG%
) else (
    echo ❌ ERROR: No se generó el diagrama. Ver log: %LOG%
)

pause
