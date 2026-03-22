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

### 4. Migración de Funciones (Sitio Anterior / Legacy)
- [ ] **Módulo de Blog/Noticias:** Recrear en Hugo el sistema de noticias (ej: *Felices Navidades 2021*, *Aniversarios*) bajo el directorio `/content/blog/`.
- [ ] **Módulo de Páginas Institucionales:** Migrar las páginas "Código de Conducta", "Cómo ser miembro", "Contactos Regionales" y "Compromiso Social".
- [ ] **Gestión de Usuarios Activos:** Crear una página de directorio o "Nuestra Comunidad" para destacar perfiles de usuarios.

### 5. Backend CMS Headless (Gestor de Contenido Vía Web)
- [ ] **Integración de Static CMS / Decap CMS:** Crear interfaz gráfica que permita a editores y redactores de Ubuntu Venezuela publicar contenido desde un panel web (`/admin`).
- [ ] Configurar flujo de inicio de sesión de autores.
- [ ] **Colección de Noticias (Blog):** Configurar campos para imágenes de portada, título, fechas y cuerpo del artículo.
- [ ] **Colección de Miembros y Roles:** Configurar en el CMS la posibilidad de añadir usuarios creando "tarjetas de perfil" con selectores de roles (`badges`) como: "Conferencista", "Contacto Local", "Miembro LoCo". El CMS generará esto en Hugo para mostrar un directorio del equipo.

### 6. Sistema Funcional para Usuarios y Eventos
- [ ] **Sistema de Registro de Eventos:** Como Hugo es estático, integrar un gestor de formularios serverless (Formspree, Netlify Forms o Supabase) que permita a los asistentes llenar un formulario en la web de Ubuntu-Ve y guardar sus datos automáticamente en una base de datos o tabla segura, sin comprometer el servidor principal.
- [ ] Crear el layout visual (`partials` o `shortcodes`) de "Tarjeta de Evento" con su botón respectivo para incrustar el formulario de registro.
- [ ] Elaborar la lógica que relaciona Eventos y Conferencistas para renderizar automáticamente perfiles de oradores.

### 7. Automatización de Noticias (RSS / Scraping)
- [x] **Script Agregador de Noticias:** Desarrollar un script en Python (ej. `fetch_news.py`) que consuma el RSS oficial del Blog de Ubuntu o sitios confiables relacionados.
- [x] **Generador Markdown:** Hacer que el script procese las noticias y genere archivos `.md` estructurados en la carpeta de Hugo con su fecha, título y enlace a la fuente original.
- [ ] **Traducción Automática:** (Opcional) Evaluar el uso de una API para traducir automáticamente el extracto si la fuente está en inglés.
- [ ] Integrar un Cron Job (ej. en GitHub Actions) para que este script se ejecute diariamente o semanalmente y mantenga viva la página de noticias sin intervención manual.
- [ ] Integrar un Cron Job (ej. en GitHub Actions) para que este script se ejecute diariamente o semanalmente y mantenga viva la página de noticias sin intervención manual.

### 8. Verificación y Despliegue Configuración Final
- [ ] Integrar GitHub Actions para despliegue automático hacia GitHub Pages o servidor designado en cada guardado del CMS / Script.
- [ ] Ejecutar `hugo` para verificar que el build no tenga errores de preprocesado.

### 9. Creador de Certificados y Eventos (Integración Python)
- [ ] Analizar e integrar el script Python/Streamlit independiente del usuario (`cdc` / Generador de certificados rápidos: 3000 en 3min).
- [ ] No alterar la lógica CORE del generador de certificados existente. Solo crear el puente/interfaz (Web o CLI controlada) para usarlo en flujo de eventos de la comunidad.
- [ ] **Mailing con Resend:** Diseñar plantillas de correo en Resend para la bienvenida de asistentes y despacho de certificados autogenerados.

### 10. Multimedia y Reproductor de Radio (Ubuntu-Ve Radio)
- [ ] Desarrollar un "Reproductor Minimalista" global persistente (en todas las vistas del sitio).
- [ ] Integrar streaming / scraping / API desde Last.fm u otra fuente de origen (ej: Icecast) para mantener viva la Radio de Ubuntu Venezuela.
- [ ] Soportar compartir la reproducción: podcasts, audios propios y URLs.

### 11. Redes Clásicas y Modernización de Vistas
- [ ] **Sponsors / Patrocinantes:** Migrar del sitio web heredado la sección completa de sponsors y renderizarla utilizando componentes de "Cards" (tarjetas) de Vanilla Framework, ordenados de mayor a menor aporte.
- [ ] Integrar un acceso claro o visor embed para el canal **IRC** (la "vieja escuela" debe tener una puerta de entrada directa, quizá un webchat integrado o un enlace que abra un cliente configurado).
- [ ] Mejorar las tarjetas de la Frontpage (Redirecciones externas a la Wiki, Foro, etc.) para que muestren la iconografía correcta y estén bien espaciadas.

---
*Última actualización: 2026-03-22*
