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
- [x] Revisar el tema (`themes/ubuntukr`) para detectar textos "quemados" en el HTML de los layouts.

### 4. Migración de Funciones (Sitio Anterior / Legacy)
- [x] **Módulo de Blog/Noticias:** Recrear en Hugo el sistema de noticias (ej: *Felices Navidades 2021*, *Aniversarios*) bajo el directorio `/content/noticias/`.
- [ ] **Diseño Tipo Discourse (Blog/Noticias):** Modificar la vista de Noticias para que luzca y reaccione como el foro limpio de *discourse.ubuntu.com*, orientándolo a hilos, etiquetas y actividad.
- [x] **Módulo de Páginas Institucionales:** Migrar las páginas "Código de Conducta" y "Compromiso Social".
- [x] **Cómo Ser Miembro / Ubuntu Membership:** Recrear las secciones de `NuevosMiembros` y `/miembroubuntu` explicando el proceso local y global.
- [ ] **Firma del Código de Conducta:** En el sitio anterior se usaba `/firma`. Implementar un mecanismo (puede ser Netlify Forms o Supabase) para registrar a quienes firman el CoC de la comunidad.
- [ ] **Contactos Regionales:** Reemplazar las redirecciones a la Wiki por una página interna dinámica que liste a los contactos por estado.
- [ ] **Galería Histórica:** El antiguo sitio redirigía a *Picasaweb* (obsoleto). Crear un nuevo layout en Hugo (ej. `layouts/gallery/`) usando una grilla CSS limpia para revivir fotos históricas y de eventos.
- [ ] **Actas / Reuniones:** Migrar logs de reuniones (`/aggregator/sources/3`) a una nueva taxonomía o sección de actas.

### 5. Backend CMS Headless y Búsqueda
- [ ] **Integración de Static CMS / Decap CMS:** Crear interfaz gráfica que permita a editores y redactores publicar contenido desde un panel web (`/admin`). Reemplaza el OpenID antiguo del Drupal.
- [ ] Configurar flujo de inicio de sesión de autores.
- [ ] **Colección de Noticias (Blog):** Configurar campos para imágenes de portada, título, fechas y cuerpo del artículo.
- [ ] **Colección de Miembros y Roles:** Configurar en el CMS la posibilidad de añadir usuarios creando "tarjetas de perfil".
- [ ] **Buscador Estático (Search API):** El Drupal tenía "Formulario de Búsqueda". En Hugo, integrar `Pagefind`, `Fuse.js` o `Lunr.js` para tener un buscador global sin necesidad de un backend tradicional.

### 6. Sistema Funcional para Usuarios y Eventos
- [ ] **Sistema de Registro de Eventos:** Interfaz serverless para reemplazar módulos de asistencia de Drupal.
- [ ] Crear layout visual de "Tarjeta de Evento" y botones para incrustar formularios.
- [ ] Relacionar Eventos y Conferencistas para renderizar perfiles automáticamente.

### 7. Automatización de Noticias (RSS / Scraping)
- [x] **Script Agregador de Noticias:** Desarrollar un script en Python.
- [x] **Generador Markdown:** Procesado a archivos `.md` de Hugo.
- [ ] **Traducción Automática:** (Opcional).
- [ ] Integrar un Cron Job (ej. en GitHub Actions) para ejecución periódica de `fetch_news.py`.

### 8. Verificación y Despliegue Configuración Final
- [ ] Integrar GitHub Actions para despliegue automático hacia GitHub Pages o servidor designado en cada guardado del CMS.
- [ ] Ejecutar `hugo` para verificar que el build no tenga errores de preprocesado.

### 9. Creador de Certificados y Eventos (Integración Python)
- [ ] Analizar e integrar el script Python/Streamlit (`cdc`).
- [ ] Mantener interfaz (Web o CLI) simple.
- [ ] **Mailing con Resend:** Diseñar plantillas de correo.

### 10. Multimedia y Reproductor de Radio (Ubuntu-Ve Radio)
- [ ] Desarrollar un "Reproductor Minimalista" global persistente (en todas las vistas del sitio).
- [x] Integrar player minimalista estático en el Footer.
- [ ] Soportar compartir la reproducción (metadatos OGG/Icecast).

### 11. Redes Clásicas y Modernización de Vistas
- [ ] **Sponsors / Patrocinantes:** Migrar la sección en tarjetas (Cards) de Vanilla Framework.
- [ ] Integrar un acceso claro al canal interactivo (Webchat IRC / Matrix / Telegram).
- [ ] Mejorar las tarjetas de la Frontpage (Redirecciones a Descargas y Foros, actualizando links muertos como Ubuntu One o Brainstorm por equivalentes modernos).

---
*Última actualización: 2026-03-22*
