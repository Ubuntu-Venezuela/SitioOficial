# SPEC — Auditoría Sitioo Oficial Ubuntu-Ve (2026-09)

> Spec derivado de la auditoría técnica del sitio `SitioOficial` (Hugo/Ubuntu Venezuela) el 2026-09-09.
> Declarado en SLP_HOME (`spec-files.json`, modo `track`). Este documento es el `spec_doc` del gate SPEC.

## Criterios de Aceptación (gate SPEC)

- [ ] P0 resuelto: CNAME correcto (`ubuntu-ve.org`), sin rutas 404 de producción, despliegue único definido (Netlify `public/`).
- [ ] P1 resuelto: assets de marca/avatares presentes, `/eventos/` funcional, `certificado.py` corre sin TabError, páginas EN no vacías.
- [ ] P2 resuelto: capturas publicadas desde `static/`, miniaturas de noticias no vacías, buscador operativo, contactos y repo fuente consistentes.
- [ ] P3 resuelto: sin placeholders muertos, sin textos coreanos, slides EN al día.

## Mapa de Prioridades (orden de trabajo)

### P0 — URGENTE (producción / branding)
| # | Issue | Archivos afectados |
|---|-------|--------------------|
| 1 | `CNAME` apunta a `ubuntu-uk.org` (dominio erróneo, marca de otro LoCo) | `static/CNAME`, `docs/CNAME` |
| 2 | Botón slide "Únete a nosotros" → `/community` 404 (`.RelPermalink` vacío en range) | `layouts/index.html`, `content/slides/comunidad-ve/index.md` |
| 3 | Carpeta `docs/` (build GH Pages, 149 archivos) commiteada — contradice `netlify.toml` (publish `public`) | `docs/**`, `netlify.toml` |

### P1 — ALTO (funcionalidad y marca)
| # | Issue | Archivos afectados |
|---|-------|--------------------|
| 4 | Hero roto: `UbuntuKrCircleTag.svg` no existe | `static/img/UbuntuKrCircleTag.svg`, `layouts/index.html` |
| 5 | Avatares fallback inexistentes: `logo.png`, `default-avatar.png` | `static/img/logo.png`, `static/img/default-avatar.png`, `layouts/miembros/*`, `layouts/noticias/list.html` |
| 6 | `/eventos/` en menú y home → 404 (no existe `content/eventos/`) | `config.yaml`, `content/eventos/**`, `layouts/eventos/single.html` |
| 7 | `certificado.py` falla con `TabError` (tab+espacios L26) + `rstrip` sin asignar | `certificado/certificado.py` |
| 8 | 3 páginas EN vacías (0 bytes) | `content/sponsors/_index.en.md`, `content/translate/index.en.md`, `content/try/index.en.md` |
| 9 | Noticias EN byte-idénticas al español (sin traducción real) | `content/noticias/**` |

### P2 — MEDIO (calidad y despliegue)
| # | Issue | Archivos afectados |
|---|-------|--------------------|
| 10 | Capturas del home en `screenshot/` del repo, no publicadas en `static/` | `static/screenshot/**`, `layouts/index.html` |
| 11 | `fetch_news.py`: `thumbnail: ""` en 89 noticias + URLs con doble slash (`//blog/`) | `scripts/fetch_news.py`, `content/noticias/**` |
| 12 | Pagefind declarado en `<head>` pero nunca construido → buscador roto | `themes/ubuntukr/layouts/**`, `netlify.toml` |
| 13 | `mailto:junta@ubuntu.org.ve` ≠ `junta@ubuntu-ve.org` | `layouts/about/list.html` |
| 14 | `source_repo` apunta a repo equivocado (`ubuntu-ve/ubuntu-ve.github.io`) | `config.yaml` |

### P3 — BAJO (pulido)
| # | Issue | Archivos afectados |
|---|-------|--------------------|
| 15 | Radio con placeholder muerto (`stream.last.fm/your-stream-url`) | `config.yaml` |
| 16 | Botón "Nueva Noticia" con `href="#"` muerto | `layouts/noticias/list.html` |
| 17 | Textos coreanos (`후원사`, etc.) en el tema sin traducir | `themes/ubuntukr/layouts/**` |
| 18 | Slides EN desactualizados (dice 23.10, el ES dice 24.10) | `content/slides/ubuntu/index.en.md` |

## Declaración SLP

- `spec`: auditoria-sitio-2026-09
- `mode`: track
- `declared`: 27 paths (ver `spec-files.json` en SLP_HOME) — cubre todos los archivos del mapa de prioridades.

---
*Creado: 2026-09-09 — estado de partida: 0/27 certificados, todo `[S] planned`.*