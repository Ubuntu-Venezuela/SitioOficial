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
    `http://www.ubuntu-ve.org/radio`. → BLOQUEADO: necesita URL real del stream
    de la comunidad (Icecast/Shoutcast .mp3) antes de tocar `config.yaml`.

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

## F5 — Scripts

- `certificado/certificado.py`: TabError L26 + `rstrip` sin asignar.
- `fetch_news.py`: thumbnails vacíos, doble slash en URLs.

## F6 — Verificación

- `hugo --gc --minify` sin errores.
- `slp_lens_status` + `slp-tree`: archivos pasan a certified.
- Commit con identidad configurada.