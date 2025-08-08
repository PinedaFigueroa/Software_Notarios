# README - Librerías Necesarias Agregadas (05/08/25)

**Proyecto:** Software Notarios  
**Autor:** Giancarlo Figueroa + Tars-90  
**Motivo:** Documentación de dependencias y problemas encontrados al instalar librerías en Windows 10/11 con Python 3.13

---

## 1. Contexto

Se requería un entorno completo para:

1. Generar diagramas ER de la base de datos (`eralchemy2`, `graphviz`, `pygraphviz`)
2. Exportar a **Excel y PDF** (`pandas`, `openpyxl`, `PyMuPDF`, `reportlab`)
3. Manejar documentos **Word** (`python-docx`, `docx2pdf`)
4. Preparar **documentación técnica** con `Sphinx`
5. Futuro uso con **chatbot OpenAI** (`openai`, `tiktoken`)
6. Compatibilidad **Windows / Python 3.13** evitando compilación nativa

---

## 2. Problemas encontrados

1. **Error al instalar `pandas`**:
meson.build:2:0: ERROR: Compiler cl cannot compile programs 


- Causa: Pandas intentaba compilar código fuente (`pyproject.toml`) porque **no existía wheel compatible con Python 3.13**.

2. **Dependencias como `pygraphviz` y `pandas`** fallaron por ausencia de **Visual C++ Build Tools**.

---

## 3. Solución aplicada

1. **Actualizar pip, setuptools y wheel**  
2. **Instalar primero numpy** con `--only-binary :all:`  
3. Ajustar versión de **pandas a 2.2.1**  
4. Usar **wheel local** para `pygraphviz` compatible con Python 3.13  
5. Crear `requirements_full_windows.txt` completo y optimizado

---

## 4. Resultado

- Todas las librerías se instalaron correctamente en el entorno virtual `swnot`  
- Se puede ejecutar `generate_db_docs.bat` sin errores de librerías  
- Próximo paso: probar generación de diagramas y Excel

---
@echo off
REM ====================================================
REM  Software Notarios - Generación de Documentación BDD
REM  Fecha: 05/08/2025
REM  Autor: Giancarlo + Tars-90
REM  Objetivo: Crear listados de tablas/variables y diagramas
REM ====================================================

echo Creando carpetas de documentacion...
mkdir db_docs
mkdir db_docs\Listados
mkdir db_docs\Diagramas

echo Generando listados de tablas y columnas en Excel...
python - <<EOF
import pandas as pd
from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql+psycopg2://postgres:12345678@localhost/software_notarios')
insp = inspect(engine)

data = []
for table in insp.get_table_names():
    for col in insp.get_columns(table):
        data.append({
            "Tabla": table,
            "Columna": col["name"],
            "Tipo": str(col["type"]),
            "Primary Key": col.get("primary_key", False)
        })

df = pd.DataFrame(data)
excel_path = "db_docs/Listados/BDD_Listado_050825.xlsx"
df.to_excel(excel_path, index=False)
print(f"Archivo Excel generado en {excel_path}")
EOF

echo Generando diagrama ER en PNG y PDF...
eralchemy -i postgresql+psycopg2://postgres:12345678@localhost/software_notarios -o db_docs\Diagramas\ERD_050825.png
eralchemy -i postgresql+psycopg2://postgres:12345678@localhost/software_notarios -o db_docs\Diagramas\ERD_050825.pdf

echo Documentacion generada correctamente en db_docs\
pause
