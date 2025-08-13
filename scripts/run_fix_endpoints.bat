@echo off
REM archivo: scripts\run_fix_endpoints.bat (actualizado 13/08/25 hora 01:09)
setlocal
set ROOT=%~dp0..\..
echo Ejecutando fix_endpoints.py en %ROOT%
python "%~dp0fix_endpoints.py" "%ROOT%"
echo Listo.