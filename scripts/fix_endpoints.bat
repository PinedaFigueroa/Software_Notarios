:: archivo: scripts\fix_endpoints.bat
:: última actualización: 13/08/25 hora 00:52
:: motivo: Wrapper para ejecutar el script PowerShell de corrección de endpoints
:: autor: Giancarlo + Tars-90
@echo off
setlocal
set ROOT=%~dp0..\..
echo Ejecutando corrección de endpoints en %ROOT%
powershell -ExecutionPolicy Bypass -File "%~dp0fix_endpoints.ps1" -Root "%ROOT%"
echo Listo.