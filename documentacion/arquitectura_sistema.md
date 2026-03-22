# Arquitectura y Contexto del Sistema - Ubuntu Venezuela

Este documento centraliza el conocimiento arquitectónico, decisiones técnicas y la estructura de datos del portal web oficial de Ubuntu Venezuela. Actúa como la "biblia del conocimiento" para asegurar la continuidad y coherencia en el desarrollo del sitio estático con Hugo.

## 1. Persistencia de Datos y Arquitectura (Jamstack / Headless)

El portal abandona los CMS tradicionales monoclíticos (como Drupal) en favor de una arquitectura moderna basada en **Jamstack** (JavaScript, APIs y Markup), usando **Hugo** como generador de sitios estáticos. La persistencia de datos se divide en dos capas principales según la naturaleza del contenido:

### 1.1. Contenido Editorial e Institucional (Persistencia en Git)
Todo el contenido público del sitio no usa una base de datos de servidor tradicional (como MySQL o PostgreSQL). En su lugar, se almacena **directamente en el repositorio de GitHub** (`Ubuntu-Venezuela/SitioOficial` en la rama `main`) utilizando carpetas con archivos **Markdown (`.md`)**.

Esto incluye:
*   **Noticias y el Blog** (`/content/noticias/`).
*   **Directorio de Comunidad y Conferencistas** (`/content/miembros/`).
*   **Información de Eventos y Patrocinadores** (`/content/eventos/`, `/content/sponsors/`).
*   **Páginas fijas** (Como "Sobre Nosotros", "Comunidad", etc.).

**Panel de Administración (Decap CMS / Static CMS):**
Los editores no requieren saber programación. Cuando un redactor escribe una noticia desde la interfaz gráfica web (`/admin`), el CMS interactúa con la API de GitHub para crear un "commit" y guardar automáticamente los cambios en el archivo `.md`, construyendo el sitio de manera transparente.

**Beneficios de esta capa:**
*   **Seguridad:** Al no existir una base de datos conectada en tiempo real al frontend, evitamos ataques de Inyección SQL.
*   **Desempeño:** Las páginas pre-renderizadas son servidas mundialmente por un CDN extremadamente rápido.
*   **Control de Cambios:** Podemos revertir una nota borrada usando el historial natural de Git.

### 1.2. Datos Dinámicos y de Usuarios (Persistencia Serverless / BaaS)
Puesto que Hugo es un generador de páginas pre-creadas, no procesa sesiones PHP o Python por sí mismo en el momento de la visita del usuario. Para los datos transaccionales, formularios interactivos y registros de la comunidad, el sistema delega la función a servicios en la nube de tipo Backend as a Service (BaaS) e interfaces Serverless.

*   **Firma del Código de Conducta (CoC):** Se utilizará una solución externa como **Netlify Forms**, o bases de datos orientadas a servicios modernos (como **Supabase** o **Firebase**). Dichos servicios proveerán el endpoint mediante el cual el HTML enviará los registros.
*   **Asistencia y Registro de Eventos:** Interfaz Serverless (pequeñas API / "Functions") ejecutadas en la nube tras presionar "Registrarme", las cuales persisten la asistencia en una base de datos externa tipo Supabase.
*   **Creador de Certificados (Script Pytnon `cdc`):** Se alimentará localmente o mediante la carga de planillas estructuradas como archivos Excel (`.xls` o `.csv`) que fungen como origen de datos temporal.
 
De esta forma, conservamos la estabilidad del sitio pero podemos añadir infinitas características dinámicas montando "APIs invisibles" con servicios Serverless.

---
*Nota: Este documento debe ser actualizado cada vez que se agregue una capa nueva u ocurra un cambio relevante en la forma en que el sitio gestiona información.*
