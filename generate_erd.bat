@echo off
echo Generando diagrama ERD...
eralchemy2 -i "postgresql://postgres:12345678@localhost:5432/software_notarios" -o docs/erd.pdf
echo ERD generado en docs/erd.pdf
pause
