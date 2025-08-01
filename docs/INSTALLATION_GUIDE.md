# 📘 Guía de Instalación – Software Notarios

Esta guía explica cómo inicializar la base de datos para **desarrollo o producción**.

---

## 1. Requisitos

- PostgreSQL 17+  
- Python 3.10+  
- Variables de entorno configuradas:
  - `PG_USER` (ej: `postgres`)
  - `PG_PASSWORD` (si aplica)
  - `PG_HOST` (ej: `localhost`)
  - `PG_PORT` (ej: `5432`)
  - `PG_DB_NAME` (ej: `software_notarios_dev`)

---

## 2. Inicialización en Windows (Recomendada)

1. Ejecutar **como Administrador**:


2. Seguir los pasos en pantalla:
   - Confirmar con **S/s** si desea reinicializar
   - Si la base existe, decidir si eliminarla

3. Verificar el log en `errores_bdd_flask`

---

## 3. Inicialización en Linux/Mac

1. Activar el entorno virtual y ejecutar:

python scripts/init_big_bang_2_v5.py

2. Confirmar pasos S/N en consola  
3. Revisar logs en `errores_bdd_flask`

---

## 4. Producción

- **No usar pgAdmin para crear la DB manualmente**  
- Usar el mismo procedimiento del `.bat` o `.py` para garantizar:
  - `UTF8`
  - `template0`
  - `LC_COLLATE='C'` y `LC_CTYPE='C'`

---

## 5. Logs y soporte

Todos los errores y decisiones del operador se registran en:

C:\Users\Usuario\Mi unidad\Software_Notarios\errores_bdd_flask


- `drop.log` → Eliminación de DB  
- `create.log` → Creación de DB  
- `upgrade.log` → Migraciones  
- `seed.log` → Seed inicial
- `big_bang_2_v5.log` → Bitácora completa del proceso

---

## 6. Consejos finales

- Ejecutar los scripts desde la raíz del proyecto  
- Mantener backups de la carpeta `errores_bdd_flask` para auditoría  
- Validar siempre que la DB quede en `UTF8 | C | C` usando `\l` en `psql`  
