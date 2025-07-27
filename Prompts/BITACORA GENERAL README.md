💙🛠️✨ **Listo navegante, aquí va tu README.md completo**
*(markdown limpio, listo para copiar/pegar en tu repo o VS Code, lo dejo completo en bloque)*

---

## 📦 `README.md`

````markdown
# 🚀 Software_Notarios

> Sistema modular para bufetes jurídicos y notarios: multi-usuario, multi-rol, auditoría, feature flags, almacenamiento en nube, dashboards, CRM/ERP, documentación técnica y manual de usuario.

---

## ✅ Tecnologías clave
- Python 3.13 (64 bits)
- Flask + SQLAlchemy
- Alembic (Flask-Migrate)
- PostgreSQL
- Sphinx (doc técnica)
- MkDocs (manual usuario)
- ERAlchemy2 (diagramas ER)
- Frontend (por definir: React, etc.)

---

## 🛠 Instalación local

```bash
# 1) Crear entorno virtual
python -m venv swnot
swnot\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt
````

---

## ⚙ Base de datos

* PostgreSQL ≥ 17
* Crear base de datos `software_notarios` con UTF8
* Usuario por defecto: `postgres` / `12345678`
  *(configurable)*

---

## 🌱 Seed inicial (Big Bang)

```bash
init_dev_db.bat
```

Este script:

* Elimina y crea la BDD
* Inicializa Flask-Migrate
* Ejecuta migraciones
* Inserta datos iniciales:

  * Plan Starter
  * Bufete principal
  * Notario principal
  * Usuario superadmin (`admin@bufete.com`)

---

## 🔄 Cambios en modelos

Cuando modifiques modelos:

```bash
python -m flask db migrate -m "Describe change"
python -m flask db upgrade
```

---

## 📊 Diagrama entidad-relación (ER)

```bash
eralchemy2 -i "postgresql://postgres:12345678@localhost:5432/software_notarios" -o docs/erd.pdf
```

Genera `docs/erd.pdf` con todas las tablas y relaciones.

---

## 📑 Documentación técnica (Sphinx)

```bash
pip install sphinx
cd docs
sphinx-quickstart
sphinx-apidoc -o source ../app
make html
```

HTML generado en `docs/build/html`.

---

## 🧭 Manual de usuario (MkDocs)

```bash
pip install mkdocs mkdocs-material
mkdocs new .
mkdocs serve
```

Visualiza localmente en `http://127.0.0.1:8000`.

---

## ✅ Checklist buenas prácticas

* `pip freeze > requirements.txt`
* `git add .`
* `git commit -m "feat: cambio X"`
* `git push`
* Mantener diagrama ER actualizado
* Documentar nuevos módulos en Sphinx
* Actualizar manual usuario en MkDocs

---

## 📌 Roadmap resumido

* CRUD para bufetes, notarios, procuradores, asistentes
* Feature flags y planes flexibles
* Librería de cláusulas y documentos
* Control de costos y dashboard
* CRM/ERP ligero
* Machine learning futuro (basado en datos históricos)
* Firma electrónica
* Control de login, auditoría, trazabilidad

---

## 🙏 Bendición

> “Todo lo puedo en Cristo que me fortalece” ✝️
> Con orden, visión y fe este software será de bendición a muchos.

---

👨‍💻 by *Pineda von Ahn & Tars-90 (IA co-pilot)*

````

---

## ✅ **Te incluyo también la estructura sugerida:**
```plaintext
Software_Notarios/
├─ app/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ core.py
│  ├─ config.py
│  └─ (otros módulos)
├─ docs/
│  ├─ erd.pdf
│  ├─ (sphinx files)
│  └─ (mkdocs files)
├─ init_dev_db.bat
├─ requirements.txt
├─ migrations/
├─ README.md  ← este archivo
└─ .gitignore
````

---

🔥 **¿Quieres que te empaquete ahora mismo un zip** con:
✅ README.md
✅ doc inicial Sphinx
✅ mkdocs.yml
✅ estructura de carpetas?

Responde **"sí zip"** y lo armo para que descargues directo, navegante 🚀⚓
