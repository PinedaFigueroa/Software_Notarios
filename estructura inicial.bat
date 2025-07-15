REM crea estructura inicial de directorios
REM 14 - 07 - 25  19:42

mkdir app
cd app
mkdir models templates static
cd models
echo "" > __init__.py
echo "" > enums.py
echo "" > core.py
echo "" > documentos.py
echo "" > clausulas.py
echo "" > bienes.py
echo "" > expedientes.py
echo "" > timbres.py
echo "" > facturacion.py
echo "" > relaciones.py
echo "" > entidades.py
cd ..
echo "" > __init__.py
echo "" > cli.py
echo "" > config.py
echo "" > routes.py
cd ..
mkdir migrations

