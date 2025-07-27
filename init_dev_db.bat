@echo off
echo Ejecutando inicializador de entorno de desarrollo (Python)...

REM Ejecutar con ruta entre comillas para evitar error por espacios
python "C:\Users\Usuario\Mi unidad\Software_Notarios\scripts\init_dev_db.py"

IF %ERRORLEVEL% NEQ 0 (
    echo Error al ejecutar init_dev_db.py
    echo Revisa el archivo init_error.log para mas detalles.
) ELSE (
    echo Proceso completado correctamente.
)

pause
