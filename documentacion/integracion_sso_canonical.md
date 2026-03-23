# Integración: Canonical SSO, Launchpad y Discourse (Validación Server-Side)

Este documento detalla la arquitectura y el funcionamiento de la "Verificación Oficial y Perfiles de Miembros", implementada en la página `/miembros/` para mostrar el status real de cada voluntario en el ecosistema mundial de Ubuntu.

## 1. Arquitectura "Server-Side" (Libre de CORS)

Para evitar bloqueos de origen cruzado (CORS), limitaciones en llamadas de red por navegador y carga lenta de la interfaz, la validación **no se ejecuta en JavaScript (del lado del cliente)**.

Toda la obtención de datos se hace en tiempo de construcción (Server-Side) nativamente a través del generador estático Hugo, mediante su función `resources.GetRemote`.
*   Cuando Hugo reconstruye el sitio (por un push o por el arranque del servidor), acude a las APIs de Discourse y Launchpad.
*   Acopla los JSON de respuestas y escribe estáticamente el HTML resultante para el visitante.
*   Esto asegura una arquitectura sumamente segura, escalable e hiper-veloz.

## 2. Orígenes de Datos Soportados

El sistema revisa qué llaves (variables) tiene declaradas un miembro en su archivo Markdown (`/content/miembros/miembro.md`) y procede a hidratar su perfil:

### A. Discourse / Canonical SSO (`discourse: "username"`)
*   **Endpoint:** `https://discourse.ubuntu.com/u/USERNAME.json`
*   **Datos que extrae:**
    *   Verificación de si el usuario pertenece al grupo o título ("flair") `ubuntumembers`.
    *   Listado de Badges recibidos en los Foros de Ubuntu.
*   **Efecto Visual:** Si es miembro oficial, se inyecta la cinta `MIEMBRO CANONICAL` y se colorea de morado. Adicionalmente, se renderizan al fondo sus insignias de Discourse.

### B. Plataforma Launchpad (`launchpad: "username"`)
*   **Endpoint:** `https://api.launchpad.net/1.0/~USERNAME`
*   **Datos que extrae:**
    *   `is_ubuntu_coc_signer`: Boleano para confirmar si tiene el Código de Conducta (CDC) firmado a nivel mundial.
    *   `mugshot_link` o `logo_link`: Extrae dinámicamente el URL directo de la foto del usuario en los repositorios de Launchpad.
    *   `karma`: Puntos de contribución del usuario.
*   **Efecto Visual:** Rellena la fotografía oficial de la tarjeta (anulando la necesidad de que el usuario suba una). Concede el tag `ACTIVO (CDC)`. Muestra los puntos absolutos de Karma en el perfil extendido.

## 3. Comportamiento Modular (Fallbacks)

El generador de perfiles es tolerante a fallos:
*   Si la API se cae o responde 404 porque alguien configuró mal el nombre, **el layout no se rompe**.
*   El avatar recae silenciosamente en `onerror="... default-avatar.png"` o usa el avatar local por defecto del directorio `/img/`.
*   Si no es un miembro reconocido globalmente, su tarjeta simplemente reflejará el status local asignado (ej: *Miembro LoCo*).

## 4. Troubleshooting: Bloqueos de Aprobación por parte de GitHub (Decap CMS)

La interfaz estática (**Decap CMS**) permite a cualquier voluntario designado inyectar visualmente su nombre de Launchpad o Discourse.
Para que esto funcione con el modelo "Serverless Git-Gateway", la aplicación que autentica (usualmente "Netlify Identity" o el "OAuth App" propio) tiene permisos para escribir por la API en la rama de Github.

**Problema común (Avisos Rojos "API_ERROR... access restrictions"):**
Al estar el código guardado bajo una Organización corporativa de GitHub (`@Ubuntu-Venezuela`), GitHub bloquea aplicaciones de terceros por defecto.

**Solución por Administrador:**
1.  Ingresar como Administrador (Owner) del Github de la Organización.
2.  Navegar a **Settings** de la Organización.
3.  Ingresar a **"Third-party Access"** (dentro del panel *OAuth application policy*).
4.  Buscar la App que reporta el rechazo y dar clic en el botón de **Approve** / **Grant Access**.
5.  Actualizar la página del Editor CMS.

A partir de este flujo de aprobación, la comunidad podrá autor-gestionar completamente el directorio web desde la interfaz gráfica o contribuyendo directamente el archivo en Git.
