# Software Notarios - Bloque 1: Base de Datos y Seeds
## Fecha: DD/MM/AAAA

### ✅ Avances
- DB reinicializada con `init_dev_db`
- Migraciones aplicadas sin errores
- Seed inicial ejecutado:
  - Roles creados (Superadmin, Admin Local, Notario, Procurador, Asistente)
  - Bufete principal y notario principal creados
  - Cláusulas y puntos iniciales insertados

### 🐞 Errores y Soluciones
- (Ejemplo) Error en `flask db migrate` por `alembic_version` heredada → Solución: usar DROP DB con FORCE y limpiar `migrations`

### 📄 Código y Comandos Importantes
- `init_dev_db.bat`  
- `python -m scripts.seed_inicial`  
- `flask shell` → Verificación de roles y bufetes

### 📌 Pendientes
- Confirmar test de relaciones (`test_relaciones_asociacion.py`)  
- Verificar inserción correcta de todas las cláusulas/puntos
