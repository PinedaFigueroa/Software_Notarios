# Proyecto: Software Notarios | Bloque 4 - Documentos y Librería
Usuario: Giancarlo Figueroa 

Contexto:
- La aplicación debe gestionar escrituras, actas y sus cláusulas/puntos
- Tenemos modelos iniciales y enums para cláusulas y puntos
- Objetivo: CRUD de documentos notariales completo y manejo de librería

Alcance del Bloque 4:
1. Crear y probar modelos para:
   - Documentos notariales
   - ClausulasPuntos (aplican a escrituras y actas)
   - Relación documentos ↔ notarios/procuradores
2. Implementar CRUD básico:
   - Crear documento
   - Editar documento
   - Eliminar documento (borrado lógico)
3. Integrar selección de cláusulas/puntos:
   - Dropdown o buscador al crear documento
   - Clasificación: General, Obligatoria, Sugerida, Personalizada
4. Conectar con librería del bufete:
   - Guardar documentos
   - Listar por estado (Borrador, Firmado, Archivado)
   - Mostrar avisos o vencimientos
5. Generar `README diario` con:
   - Tablas y modelos creados
   - Pruebas CRUD
   - Pendientes para integrar con dashboard

Notas importantes:
- Usar `borrado_logico` para no perder historial
- Clasificar correctamente cláusulas y puntos
- Mantener relaciones consistentes entre notarios, procuradores y documentos

¡Perfecto, Giancarlo! 🙌
Vamos a trabajar el **Bloque 4 - Documentos y Librería** paso a paso, con un enfoque claro para integrar modelos, CRUD y librería.

---

### **Plan de Desarrollo Bloque 4**

#### **1. Modelos de Documentos y Librería**

Crearemos en `app/models/documentos.py`:

```python
# archivo: app/models/documentos.py
# fecha de creación: 31 / 07 / 25
# cantidad de lineas originales: 0
# última actualización: 31 / 07 / 25 hora 12:15
# motivo de la actualización: Creación de modelos de documentos y librería de cláusulas
# autor: Giancarlo + Tars-90
# -*- coding: utf-8 -*-

import datetime
from app import db
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.usuarios import Usuario

# --- ENUMS ---

class EstadoDocumentoEnum(PyEnum):
    BORRADOR = "borrador"
    FIRMADO = "firmado"
    ARCHIVADO = "archivado"

class TipoClausulaEnum(PyEnum):
    GENERAL = "general"
    OBLIGATORIA = "obligatoria"
    SUGERIDA = "sugerida"
    PERSONALIZADA = "personalizada"


# --- MODELOS ---

class DocumentoNotarial(db.Model):
    """
    Documentos notariales: escrituras, actas, etc.
    """
    __tablename__ = "documentos_notariales"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    tipo = Column(String(50), nullable=False)  # Ej: Escritura, Acta
    estado = Column(Enum(EstadoDocumentoEnum), default=EstadoDocumentoEnum.BORRADOR, nullable=False)

    # Relaciones
    notario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    procurador_id = Column(Integer, ForeignKey('usuarios.id'))
    
    notario = relationship("Usuario", foreign_keys=[notario_id])
    procurador = relationship("Usuario", foreign_keys=[procurador_id])

    clausulas = relationship("DocumentoClausula", back_populates="documento", cascade="all, delete-orphan")

    # Auditoría
    borrado_logico = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ClausulaPunto(db.Model):
    """
    Cláusulas y puntos de la librería del bufete.
    """
    __tablename__ = "clausulas_puntos"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(Enum(TipoClausulaEnum), default=TipoClausulaEnum.GENERAL, nullable=False)

    # Relación con bufete (opcional si cada bufete tiene su librería)
    bufete_id = Column(Integer, ForeignKey('bufetes_juridicos.id'))

    # Auditoría
    borrado_logico = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class DocumentoClausula(db.Model):
    """
    Relación Documento ↔ Cláusulas seleccionadas.
    """
    __tablename__ = "documento_clausulas"

    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer, ForeignKey('documentos_notariales.id'))
    clausula_id = Column(Integer, ForeignKey('clausulas_puntos.id'))

    documento = relationship("DocumentoNotarial", back_populates="clausulas")
    clausula = relationship("ClausulaPunto")

    # Orden de aparición en el documento
    orden = Column(Integer, default=1)
```

---

#### **2. Rutas CRUD básicas**

En `app/documentos/routes.py`:

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.documentos import DocumentoNotarial, ClausulaPunto, DocumentoClausula

documentos_bp = Blueprint('documentos', __name__)

# Crear documento
@documentos_bp.route('/documentos/nuevo', methods=['GET', 'POST'])
def crear_documento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        notario_id = request.form['notario_id']

        doc = DocumentoNotarial(
            titulo=titulo,
            tipo=tipo,
            notario_id=notario_id
        )
        db.session.add(doc)
        db.session.commit()
        flash('Documento creado correctamente', 'success')
        return redirect(url_for('documentos.listar_documentos'))

    return render_template('documentos/nuevo.html')


# Listar documentos
@documentos_bp.route('/documentos')
def listar_documentos():
    documentos = DocumentoNotarial.query.filter_by(borrado_logico=False).all()
    return render_template('documentos/listar.html', documentos=documentos)


# Eliminar (borrado lógico)
@documentos_bp.route('/documentos/eliminar/<int:doc_id>', methods=['POST'])
def eliminar_documento(doc_id):
    doc = DocumentoNotarial.query.get_or_404(doc_id)
    doc.borrado_logico = True
    db.session.commit()
    flash('Documento eliminado lógicamente', 'info')
    return redirect(url_for('documentos.listar_documentos'))
```

---

#### **3. Integración de Cláusulas y Librería**

* Al crear un documento, mostraremos un **dropdown o buscador** con cláusulas clasificadas.
* Guardaremos la selección en `DocumentoClausula` con `orden` para mantener secuencia.

---

#### **4. `README diario`**

Se generará un resumen con:

* Tablas creadas: `documentos_notariales`, `clausulas_puntos`, `documento_clausulas`
* CRUD implementado: crear, listar, borrar lógico
* Pendientes:

  1. Editar documento
  2. Asignación de cláusulas en la UI
  3. Mostrar avisos en dashboard

---

Si quieres, puedo **generar ahora mismo los archivos listos para descargar**:

* `models/documentos.py`
* `documentos/routes.py`
* `templates/documentos/nuevo.html` y `listar.html` de ejemplo

¿Quieres que los prepare en un **ZIP completo listo para pruebas**?
