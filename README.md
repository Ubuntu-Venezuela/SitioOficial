# Ubuntu Venezuela - Sitio Oficial (Yari-AI v6.2.0)

![Ubuntu Logo](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Hugo](https://img.shields.io/badge/Hugo-FF4088?style=for-the-badge&logo=hugo&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Operativo-success?style=for-the-badge)

EsEste es el repositorio oficial del sitio web de la comunidad **Ubuntu Venezuela (Ubuntu-Ve)**. El sitio está construido con [Hugo](https://gohugo.io) y utiliza el [Vanilla Framework](https://vanillaframework.io) para mantener la estética oficial de la marca Ubuntu.
## Vistas del Proyecto

Aquí puedes ver el estado actual del diseño y la funcionalidad del portal:

<p align="center">
  <img src="screenshot/WhatsApp Image 2026-03-21 at 11.38.51 PM.jpeg" width="30%" alt="Dashboard Local" />
  <img src="screenshot/news_discourse.jpeg" width="30%" alt="Timeline de Noticias Discourse" />
  <img src="screenshot/members_sso.jpeg" width="30%" alt="Verificación SSO Miembros" />
</p>
<p align="center">
  <img src="screenshot/WhatsApp Image 2026-03-22 at 12.13.48 AM.jpeg" width="45%" alt="Sección de Aliados" />
  <img src="screenshot/WhatsApp Image 2026-03-22 at 1.40.01 AM.jpeg" width="45%" alt="Detalle de Evento" />
</p>

## Características Destacadas (Features)

El sistema ha sido evolucionado para ser una plataforma de gestión comunitaria completa:

-   **Bot de Noticias Automatizado:** Las noticias oficiales se importan directamente simulando un hilo de Discourse. El bot obtiene, traduce y publica noticias de Ubuntu diariamente sin necesidad de intervencion manual pesada, operando bajo un tono serio, tecnico e institucional (sin usar emojis) para mantener un feed de calidad.
-   **Verificación de Perfil de Miembros (SSO Canonical):** La visualizacion de miembros de la comunidad se genera mediante un motor que consulta en Backend a Discourse y Launchpad. 
    1. Si la API de Discourse reporta al usuario como `ubuntumember`, recibe la insignia Morada de Miembro Oficial de Canonical.
    2. Si no es Oficial, pero la API de Launchpad reporta que ha firmado el Codigo de Conducta Internacional, recibe la insignia Naranja de Activista CDC.
    3. Si un miembro no porta placa alguna e incluso no le carga una foto, normalmente se debe a que el ID suministrado en su Markdown de perfil no coincide de forma exacta con su username en la plataforma externa, o nunca ha iniciado sesion activamente en ella.
-   **CMS con Workflow Editorial:** Panel administrativo (Decap CMS) con cola de aprobación. Los editores crean borradores y el Administrador aprueba antes de publicar.
-   **Generador Masivo de Certificados:** Motor Python integrado de alto rendimiento capaz de procesar 3,000 certificados en menos de 3 minutos (vía SVG a PDF).
-   **Directorio de Aliados:** Sección dinámica de patrocinadores con tarjetas resaltadas y enlaces directos a sus sitios web.

## Inicio Rápido

Para ejecutar el sitio localmente y ver los cambios en tiempo real, asegúrate de tener Hugo instalado en tu sistema.

### Requisitos previos
- **Hugo (Extended version):** Versión 0.119.0 o superior.
- **Dart Sass:** Se recomienda dart-sass-embedded para la compilación de estilos.

### Instalación y previsualización
1. Clona el repositorio:
   ```bash
   git clone https://github.com/Ubuntu-Venezuela/SitioOficial.git
   cd SitioOficial
   ```
2. Inicia el servidor de desarrollo:
   ```bash
   hugo serve
   ```
3. Visita localhost:1313 en tu navegador.

## Cómo Contribuir

Las contribuciones son bienvenidas. Si deseas ayudar a mejorar el sitio de la comunidad, sigue estos pasos:

1. Haz un Fork del proyecto.
2. Crea una rama para tu funcionalidad.
3. Realiza tus cambios y haz el commit.
4. Abre un Pull Request.

### Estructura del repositorio
- /content: Texto en formato Markdown (.md).
- /static: Imágenes, iconos y recursos descargables.
- /certificado: Motor Python de generación de diplomas.
- /scripts: Automatizaciones y bots de contenido.

## Licencia
Este proyecto está bajo la **Licencia MIT**. Los contenidos están bajo la **Licencia CC BY-SA 4.0.**

---
*Mantenido por la comunidad de Ubuntu Venezuela.*
