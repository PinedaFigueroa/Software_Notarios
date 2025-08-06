@echo off
REM =======================================================
REM Generar Documentación Sphinx para Software Notarios
REM Autor: Giancarlo + Tars-90
REM Fecha: %date% %time%
REM =======================================================

cd /d "%~dp0"

REM Carpeta base de docs
cd docs

echo ==========================================
echo 1️⃣ Limpiando build anterior...
echo ==========================================
make clean

echo ==========================================
echo 2️⃣ Generando HTML...
echo ==========================================
make html

echo ==========================================
echo 3️⃣ Generando DOCX...
echo ==========================================
make docx

echo ==========================================
echo 4️⃣ Generando PDF (si LaTeX está instalado)...
echo ==========================================
make latexpdf

REM Crear carpeta backup si no existe
if not exist "backup" mkdir backup

echo ==========================================
echo 5️⃣ Copiando resultados a /backup
echo ==========================================
xcopy /E /Y build\html backup\html\
xcopy /E /Y build\docx backup\docx\
xcopy /E /Y build\latex backup\pdf\

echo ==========================================
echo ✅ Documentación generada correctamente
echo Ubicación: docs\backup
echo ==========================================
pause
