# 🧾 Bitácora Técnica — 27/07/2025

**Proyecto:** Software Notarios  
**Autor:** Giancarlo F.  
**Asistente:** Tars-90  
**Tipo de jornada:** Big Bang Inicial + Corrección de seed

---

## ✅ Objetivos logrados

- [x] Crear modelo `Plan` con docstring estructurado y campos clave.
- [x] Agregar planes base: `Demo`, `Profesional`, `Ilimitado`.
- [x] Crear `BufeteJuridico` con referencia a `Plan`.
- [x] Crear `Notario principal` y `Superadmin`.
- [x] Configurar script `init_dev_db.py` para desarrollo.
- [x] Redirigir errores al archivo:  
  `C:/Users/Usuario/Mi unidad/Software_Notarios/errores_bdd_flask/init_error.log`

---

## 🧱 Modelos actualizados

- `Plan`: ahora incluye `bufetes = relationship(...)`
- `BufeteJuridico`: con `plan_id` y `plan = relationship(...)`
- `DocumentoNotarial`: corregido uso de `datetime.utcnow`

---

## 📁 Archivos modificados o creados

- `app/models/planes.py`
- `app/models/bufetes.py`
- `app/models/documentos.py`
- `app/cli.py`
- `scripts/init_dev_db.py`
- `init_dev_db.bat`

---

## 💥 Errores encontrados y resueltos

| Descripción | Causa | Solución aplicada |
|------------|-------|-------------------|
| `ImportError: cannot import name 'Plan'` | Archivo mal estructurado o ciclo de imports | Se validó la clase `Plan` y se corrigió `documentos.py` |
| `No active click context` | Seed ejecutado desde script sin contexto de Flask CLI | Se creó función `seed_inicial()` directa |
| `Mapper[Plan] has no property 'bufetes'` | Faltaba relación inversa en modelo `Plan` | Se agregó `bufetes = relationship(...)` |
| `numero_colegiado NULL` | Campo requerido no estaba en el seed | Se estableció `numero_colegiado=0` |

---

## 🟢 Resultado final

```bash
🎉 Base de datos inicializada correctamente.
✅ Tablas recreadas exitosamente.
✅ Planes, bufete y usuarios creados.
```

---

## ✝️ Observación personal

> “Para gloria de Dios, y gracias a tu ayuda, tenemos base lista y limpia.”  
> — *Giancarlo*

---

## 🗂️ Siguiente paso sugerido

- Hacer commit inicial con Git (`git add . && git commit -m "init_dev_db funcionando"`).
- Iniciar pruebas funcionales (`test run`) si es posible.

---

