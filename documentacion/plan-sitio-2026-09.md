# Plan de trabajo — Spec `auditoria-sitio-2026-09`

Fecha: 2026-09-09
Repo: `Ubuntu-Venezuela/SitioOficial` (main)
Despliegue: Netlify (`netlify.toml`, publish `public`, Hugo 0.124.1)

## Principios

- NO se elimina contenido (salvo información ajena a Ubuntu Venezuela).
- NO se rellena con texto genérico: investigar fuentes oficiales
  (wiki.ubuntu.com/VenezuelaTeam, ubuntu.com, loco.ubuntu.com) y personalizar.
- Modo SLP `track`: monitoreo sin bloqueo, archivos del spec avanzan a `certified`.

## F0 — Entorno de trabajo

- [x] Instalar Hugo extended v0.124.1 (zip oficial gohugoio/hugo → `C:\hugo`, PATH).
- [x] Configurar identidad git: `0xC1pher` / `alfierimorillo@gmail.com`.
- [ ] Guardar este plan en `documentacion/plan-sitio-2026-09.md`.

## F1 — Precisión de contenido

- Corregir `static/CNAME` y `docs/CNAME`: `ubuntu-uk.org` → `ubuntu-ve.org`.
- `config.yaml:15`: `source_repo` → `https://github.com/Ubuntu-Venezuela/SitioOficial`.
- Radio: investigar URL real (`ubuntu-ve.org/radio`), reemplazar placeholder
  `stream.last.fm/your-stream-url`.
  - [ ] HALLAZGO: no existe stream real en el repo ni en el historial git; el dominio
    `ubuntu-ve.org` no respondió al curl (000). La wiki oficial lista
    `http://www.ubuntu-ve.org/radio`. → PENDIENTE (decisión 2026-09-09): la
    configuración de la radio depende del área responsable de la comunidad; hay
    que preguntar a quienes manejan esa área. No tocar `config.yaml` hasta
    conseguir la URL real del stream (Icecast/Shoutcast .mp3).

## F2 — Botón "Únete a nosotros" (no eliminar)

- `layouts/index.html:34`: `<a href="{{ .url }}">` (eliminar `.RelPermalink` vacío).
- `content/slides/comunidad-ve/index.md:8` y `index.en.md:8`:
  `url: community` → `/miembro-ubuntu/`.

## F3 — Assets faltantes

- Hero: resolver `/img/UbuntuKrCircleTag.svg` (usar `static/img/logo.svg`
  o asset oficial, con marca Ubuntu-Ve).
- `default-avatar.png` / `logo.png`: generar con marca Ubuntu-Ve (SVG→PNG).

## F4 — Contenido personalizado

- Rellenar páginas EN vacías: `sponsors/_index.en.md`, `translate/index.en.md`,
  `try/index.en.md` (0 líneas) con contenido real de Ubuntu-Ve.
- Slides y noticias EN: actualizar y personalizar con datos oficiales.
  - [x] Slides ubuntu ES/EN → Ubuntu 26.04 LTS "Resolute Raccoon"
    (versión vigente verificada en releases.ubuntu.com, 2026-09-09).
  - [ ] Noticias EN (decisión 2026-09-09): NO se traducen/personalizan a mano.
    Las noticias las monta el bot existente (`scripts/fetch_news.py` +
    `.github/workflows/fetch_news_cron.yml`), que scrapea las fuentes y genera
    los archivos; se respeta ese flujo ya creado. Pendiente confirmar si el bot
    debe generar también versiones EN (hoy los `.en.md` son byte-idénticos al ES).

## F5 — Scripts

- [x] `certificado/certificado.py`: TabError L26 + `rstrip` sin asignar →
  ya corregido, compila sin errores (`python -m py_compile`).
- [x] `fetch_news.py`: thumbnails vacíos, doble slash en URLs →
  `normalize_url()` colapsa `//` duplicados; `extract_image()` usa 5
  fallbacks (media:content → enclosure → img content:encoded →
  regex jpg/png en descripción → img tag). Verificado contra feed real
  de `discourse.ubuntu.com/tag/news.rss`.

## F6 — Verificación

- `hugo --gc --minify` sin errores.
- `slp_lens_status` + `slp-tree`: archivos pasan a certified.
- Commit con identidad configurada.

## Pendientes del spec (P2/P3) — resueltos 2026-09-09

- [x] P2#10 Capturas en `screenshot/` → publicadas: copiadas a `static/screenshot/`
  (members_sso.jpeg, news_discourse.jpeg, about_page.jpeg + WhatsApp).
- [x] P2#12 Búsqueda Pagefind → activada: `package.json` (pagefind ^1.5.2) +
  `netlify.toml` command `npm run build` (hugo + pagefind --site public).
- [x] P2#13 mailto erróneo → `layouts/about/list.html` usa `junta@ubuntu-ve.org`.
- [x] P3#16 Botón "Nueva Noticia" `href="#"` → timeline Discourse del flujo que
  alimenta el bot (`https://discourse.ubuntu.com/tag/news`, `target="_blank"`).
  Corrección de feedback 2026-09-09: NO apunta a GitHub issues; usa el mismo
  flujo de noticias del bot, visible fuera del sitio.
- [x] P3#17 Textos coreanos hardcodeados del tema → traducidos al español
  (`themes/ubuntukr/layouts/sponsors/single.html`,
  `themes/ubuntukr/layouts/partials/sponsors.html`). `i18n/ko.toml` intacto
  (diccionario del idioma `ko`, legítimo).

## Sponsors y flujo de noticias — corrección de feedback 2026-09-09

- [x] P3#16bis Botón "Nueva Noticia" verificado: el timeline
  `discourse.ubuntu.com/tag/news` responde 200; el feed del category
  `c/news/40.rss` que usaba el bot responde 404 (movido).
- [x] `scripts/fetch_news.py` → feed del bot actualizado a
  `https://discourse.ubuntu.com/tag/news.rss` (200), misma fuente que el botón.
- [x] Migración de sponsors REALES de la web actual (`www.ubuntu.org.ve`,
  Drupal): Turpial (turpial.org.ve), LibreOffice Venezuela
  (libreoffice.org.ve), Mozilla Venezuela (mozillavenezuela.org) →
  `content/sponsors/{turpial,libreoffice-ve,mozilla-ve}/index.md` + logos
  descargados de la web actual. Se descartaron los sponsors coreanos
  (cloudmate, nhn-dooray, nipa_kr) ya eliminados del historial del repo
  (hitts 574830c y 9786e73) por no pertenecer a Ubuntu-Ve.
- [x] `hugo --gc --minify` OK (250 ES / 53 EN), sponsors y botón verificados
  en `public/`.

## P1#6 `/eventos/` 404 — resuelto 2026-09-09

- [x] `layouts/eventos/list.html` nuevo (grilla de tarjetas, orden por fecha desc,
  fallback en ES y EN).
- [x] `content/eventos/_index.md` + `_index.en.md`: presentación y CTA de
  organización de eventos.
- [x] Evento real de referencia `2023-06-18-feliz-17-aniversario-de-ubuntu-venezuela`
  (publicado en loco.ubuntu.com, fuente oficial de la web Drupal). Schema CMS de
  `static/admin/config.yml` respetado: title/date/location/registration_url/
  image/speakers/cert_id/cert_template/cert_list/body.
- [x] `hugo --gc --minify` OK (253 ES / 55 EN), `/eventos/` y `/en/eventos/`
  renderizados.

Pendientes abiertos: radio (depende del área responsable), noticias EN (flujo del
bot). El Discourse de la
comunidad (`discourse.ubuntu-ve.org`, DNS 69.60.114.112) no responde desde este
entorno (timeout); sponsors adicionales que viven en el Discourse/Telegram del
grupo quedan pendientes de confirmar con el área responsable.
## G3 � Seguridad panel admin + URLs muertas + dropdowns (2026-09-09) [x] 

Feedback usuario: el panel administrativo (/admin/, Decap CMS) "se ve y es
notable" y no debe exponerse asi; men� superior (Comunidad, Recursos, Descarga,
Contacto) sin opciones visibles; URLs muertas hay que arreglarlas, no eliminarlas.

- [x] Seguridad /admin/: eliminados el bot�n "Panel Administrativo (Editores)"
  de layouts/index.html y el link "Administraci�n" del footer. /admin/ sigue
  accesible por URL directa para editores (no oculto, pero sin promoci�n
  p�blica).
- [x] Dropdowns del men�: la clase .p-navigation__item--dropdown-toggle.is-active
  (que muestra el dropdown) solo la togleaba el JS de Vanilla, pero
  /js/ubuntukr.js NO existia (404). Creado
  themes/ubuntukr/static/js/ubuntukr.js con togle click/hover/teclado y cierre al
  hacer click fuera.
- [x] URL muerta /miembro-ubuntu/ (destino de slides "�nete a nosotros" y
  config join_url) no existia: creada content/miembro-ubuntu/ (ES+EN, leaf
  bundle, reusa people.jpg/logo.png) con el proceso de membres�a local y global.
- [x] href="download" relativo en home ? href="/download/" absoluto (slides de
  Ubuntu 26.04 igual).
- [x] 404: bot�n "Buscar en el sistema" apuntaba a /search (p�gina inexistente)
  ? ahora abre el search-overlay (Pagefind) igual que el nav.
- [x] hreflang EN: /en correcto (Hugo redirige /en a /en/).
- [x] Build OK y auditor�a de hrefs internos: todos resuelven a rutas v�lidas.

## G4 - Cards de sponsors y miembros rediseñados + avatares locales (2026-09-09) [x]

Feedback usuario: logos de sponsors demasiado pequeños, "mucho espacio perdido
en todos los cards", los logos deben ser clickeables, y las fotos de los
miembros "no se ven".

- [x] Sponsors (list): logo clickeable -> website (target=_blank), zona de logo
  min-height 180px fondo blanco con max-height:164px + max-width:60% +
  object-fit:contain, botón "Visitar sitio" ancho completo, fila u-equal-height.
- [x] Home partial sponsors.html: logos clickeables a .Params.website ordenados
  por Weight asc, max-height:80px.
- [x] Miembros (list): avatar 88px (antes 64px) en fondo limpio, sin alturas
  fijas (eliminados height estrictos de secciones), nombre clickeable,
  tipografías y badges recalculados, social icons 15px.
- [x] Miembros avatares 100% locales: descargados a static/img/members/<key>.png
  (discurso>launchpad mugshot) y servidos con prioridad local > discourse >
  launchpad > default-avatar en list y single. Evita fallos de GetRemote en
  build por latencia CDN y dependencias de red.
- [x] 2 miembros sin perfil (efrain-camps, wuilmer-bolivar) usan
  /img/default-avatar.png (correcto).
- [x] Build OK, avatares verificados en public (8 locales + 2 default) y sponsors
  clickeables en public/sponsors.
