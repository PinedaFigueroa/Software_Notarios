# 📌 Software para Notarios Hubsa

## 🚀 Resumen técnico del proyecto

Este proyecto busca crear una solución integral para bufetes notariales que facilite la gestión de escrituras públicas, actas notariales, control de cláusulas, documentos y costos asociados. Está diseñado para ser flexible, escalable y orientado a la nube.

## ✅ Estado actual

* Estructura inicial del repositorio creada y subida a GitHub.
* Entorno virtual configurado (`swnot`).
* Modelos principales (`core`, `enums`, etc.) definidos.
* Migraciones iniciales aplicadas y base de datos PostgreSQL creada en UTF-8.
* Seed inicial ejecutado exitosamente (creación de plan Starter, bufete principal, notario y superadmin).

## 📦 Siguientes pasos

* Desarrollar vistas (frontend) para módulos: login, dashboard, gestión de bufetes, notarios, procuradores, documentos y cláusulas.
* Añadir validadores específicos (NIT, DPI, correos, etc.).
* Implementar roles, permisos y feature flags para planes.
* Crear módulo de reportes y auditoría.
* Mejorar el proceso de seed y scripts de automatización (bash/bat).

## ⚙ Tecnologías

* Python 3 + Flask
* SQLAlchemy / Flask-Migrate
* PostgreSQL
* Git + GitHub para control de versiones
* Markdown / README para documentación

---

> ✏ Este archivo README.md puede servir como referencia y presentación general del proyecto en la raíz del repositorio.
