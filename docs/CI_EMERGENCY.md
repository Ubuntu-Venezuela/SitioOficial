# Bloqueo de CI/CD: Límite de minutos gratuitos de GitHub Actions agotado

## Estado Actual
La Integración Continua (CI) del repositorio actualmente no se está ejecutando y todos los flujos muestran un error de **`Startup failure`**.

## Causa
Se ha agotado la cuota de minutos gratuitos mensuales para ejecutar flujos de trabajo de GitHub Actions en la cuenta/organización administradora del repositorio (`Ubuntu-Venezuela/SitioOficial` o la cuenta personal usada para el despliegue). GitHub bloquea automáticamente la facturación y la ejecución de pipelines cuando se alcanza este límite si no hay forma de pago extra configurada.

## Impacto en el Sitio
1. **Despliegues Bloqueados:** El flujo principal (`hugo.yml`) no puede compilar ni publicar hacia GitHub Pages. Esto significa que los últimos arreglos están guardados en el código fuente (`main`), pero no se verán reflejados en la web accesible al público.
2. **Cron de Noticias Detenido:** El flujo programado (`fetch_news_cron.yml`) no podrá ejecutarse, por lo que las noticias en el "Planeta Ubuntu" no se actualizarán automáticamente.

## Alternativas de Solución (Alineadas con la filosofía KISS)

### Opción 1: Simplemente Esperar (La más fácil / Gratis)
Esperar a que comience el siguiente ciclo de facturación mensual de la cuenta de GitHub para que la plataforma asigne nuevamente los minutos gratuitos de Actions.

### Opción 2: Migrar el Despliegue (Sin mover el código)
Vincular este repositorio de GitHub a un servicio de alojamiento para contenido estático moderno, que utilice sus propios servidores de CI/CD (evadiendo el uso de GitHub Actions de forma 100% legal y gratis):
*   **Netlify**
*   **Cloudflare Pages**
*   **Vercel**
Cualquiera de estos servicios requiere simplemente darle acceso al repositorio, y ellos mismos corren Hugo y publican la web con límites extremadamente generosos para comunidades Open Source.

### Opción 3: Migración a GitLab (Gratis / Laborioso)
Mover el código fuente completamente a GitLab y utilizar **GitLab CI/CD** con **GitLab Pages**. GitLab otorga 400 minutos mensuales gratuitos. 
*(No se recomienda usar GitLab SÓLO para enviar de vuelta el código a GitHub Pages, ya que requiere cruzar tokens, llaves SSH y configurar mirrors, rompiendo por completo la sencillez técnica y multiplicando los puntos de falla).*

### Opción 4: Adquirir más minutos (Pago)
Ingresar a *Settings > Billing and plans* en GitHub y establecer un método de pago para cubrir el exceso en los minutos de Actions.
