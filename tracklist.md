# Plan de Transformación: Ubuntu-Ve (Tracklist)

Este archivo rastrea el progreso de la migración de la plantilla base (UK/KR) hacia el portal oficial de **Ubuntu Venezuela**.

## ✅ Tareas Completadas

### 1. Configuración de Identidad (Core)
- [x] Modificar `config.yaml`:
    - [x] Cambiar `baseURL` a `https://ubuntu-ve.org`.
    - [x] Cambiar `languageCode` a `es-ve`.
    - [x] Actualizar `title` a "Ubuntu Venezuela".
    - [x] Configurar redes sociales de Ubuntu-Ve (Twitter, Telegram, GitHub).
    - [x] Actualizar correos de contacto.
- [x] Cambiar el idioma por defecto de `en` a `es`.

### 2. Traducción y Adaptación de Contenido (`/content/`)
- [x] **About / Sobre nosotros:** Traducida y adaptada.
- [x] **Download / Descargas:** Actualizada a versiones 24.04 y 24.10.
- [x] **Community / Comunidad:** Actualizada con Telegram e IRC local.
- [x] **Sponsors / Patrocinantes:** Traducida y limpiada.
- [x] **Translate / Traducción:** Adaptada al equipo L10n-es.
- [x] **Slides / Diapositivas:** Actualizada a la versión 24.10.

## 📋 Tareas Pendientes

### 3. Personalización Visual y Assets
- [ ] Reemplazar el logo de "Ubuntu Korea/UK" por el logo de **Ubuntu Venezuela** (`static/img/logo.svg`).
- [ ] Actualizar imágenes de fondo/héroe en `static/` o `content/` con fotos de eventos locales o genéricas de Ubuntu.
- [ ] Revisar el tema (`themes/ubuntukr`) para detectar textos "quemados" en el HTML de los layouts.

### 4. Verificación y Despliegue
- [ ] Ejecutar `hugo` para verificar que el build no tenga errores de compilación de Sass.
- [ ] Validar que todos los enlaces internos funcionen.

---
*Última actualización: 2026-03-21*

