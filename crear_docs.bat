@echo off
cd /d "%~dp0docs"
set PYTHONPATH=..;.
sphinx-apidoc -o source ../app
make html
pause
