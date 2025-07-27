@echo off
echo 🌱 Iniciando estructura de documentación Sphinx...

REM Crear carpetas
mkdir docs
cd docs
mkdir modelos
mkdir modulos

echo ✅ Carpetas creadas

REM Crear index.rst
echo .. Software para Notarios documentation master file > index.rst
echo. >> index.rst
echo Software para Notarios >> index.rst
echo ======================= >> index.rst
echo. >> index.rst
echo Bienvenido a la documentación oficial de **Software para Notarios**. >> index.rst
echo. >> index.rst
echo Este sistema permite a bufetes jurídicos gestionar instrumentos públicos, actas notariales, clausulados, usuarios internos, auditoría, trazabilidad y más. >> index.rst
echo. >> index.rst
echo Documentación >> index.rst
echo ------------- >> index.rst
echo. >> index.rst
echo .. toctree:: >> index.rst
echo    :maxdepth: 2 >> index.rst
echo    :caption: Contenido >> index.rst
echo. >> index.rst
echo    introduccion >> index.rst
echo    instalacion >> index.rst
echo    configuracion >> index.rst
echo    modelos/index >> index.rst
echo    modulos/index >> index.rst
echo    api >> index.rst
echo    uso >> index.rst
echo    faq >> index.rst
echo    contacto >> index.rst
echo. >> index.rst
echo Indices y tablas >> index.rst
echo ================ >> index.rst
echo. >> index.rst
echo * :ref:`genindex` >> index.rst
echo * :ref:`modindex` >> index.rst
echo * :ref:`search` >> index.rst

echo ✅ index.rst creado

REM Otros archivos base
(for %%L in (introduccion instalacion configuracion api uso faq contacto) do (
    echo %%L > %%L.rst
    echo ======= >> %%L.rst
    echo >> %%L.rst
    echo Descripcion de %%L. >> %%L.rst
))

echo ✅ Archivos base creados

REM Crear modelos/index.rst
echo Modelos disponibles > modelos/index.rst
echo =================== >> modelos/index.rst
echo. >> modelos/index.rst
echo .. toctree:: >> modelos/index.rst
echo    :maxdepth: 1 >> modelos/index.rst
echo. >> modelos/index.rst
echo    bufete >> modelos/index.rst
echo    notario >> modelos/index.rst
echo    procurador >> modelos/index.rst
echo    asistente >> modelos/index.rst
echo    cliente >> modelos/index.rst
echo    clausula >> modelos/index.rst
echo    plan >> modelos/index.rst
echo    feature_flag >> modelos/index.rst

REM Crear plantillas modelos
(for %%M in (bufete notario procurador asistente cliente clausula plan feature_flag) do (
    echo %%M >> modelos/%%M.rst
    echo ====== >> modelos/%%M.rst
    echo >> modelos/%%M.rst
    echo Descripcion del modelo %%M. >> modelos/%%M.rst
    echo >> modelos/%%M.rst
    echo Campos >> modelos/%%M.rst
    echo ----- >> modelos/%%M.rst
    echo >> modelos/%%M.rst
    echo - id: Integer >> modelos/%%M.rst
    echo >> modelos/%%M.rst
    echo Relaciones >> modelos/%%M.rst
    echo ---------- >> modelos/%%M.rst
))

echo ✅ Modelos documentados

REM Crear modulos/index.rst
echo Modulos funcionales > modulos/index.rst
echo =================== >> modulos/index.rst
echo. >> modulos/index.rst
echo .. toctree:: >> modulos/index.rst
echo    :maxdepth: 1 >> modulos/index.rst
echo. >> modulos/index.rst
echo    autenticacion >> modulos/index.rst
echo    gestion_documentos >> modulos/index.rst
echo    facturacion >> modulos/index.rst
echo    auditoria >> modulos/index.rst

REM Crear plantillas modulos
(for %%N in (autenticacion gestion_documentos facturacion auditoria) do (
    echo %%N >> modulos/%%N.rst
    echo ====== >> modulos/%%N.rst
    echo >> modulos/%%N.rst
    echo Descripcion del modulo %%N. >> modulos/%%N.rst
    echo >> modulos/%%N.rst
    echo Caracteristicas principales >> modulos/%%N.rst
    echo -------------------------- >> modulos/%%N.rst
    echo >> modulos/%%N.rst
    echo - Detalle de %%N. >> modulos/%%N.rst
))

echo 🎉 Listo! Ahora ejecuta:
echo    make html
echo para generar la documentacion.
pause
