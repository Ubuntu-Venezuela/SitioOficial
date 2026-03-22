---
title: "Descargar Ubuntu"
description: "Puedes descargar la última versión de Ubuntu e instalarla en diversos entornos para comenzar a usarla."
image: "download.svg"
backgroundType: suru #light, dark, accent, suru, suru-topped, image
ubuntuVersions:
    ltsVersion: "24.04 LTS"
    normalVersion: "24.10"
    ltsReleaseNote: https://discourse.ubuntu.com/t/noble-numbat-release-notes/44072
    normalReleaseNote: https://discourse.ubuntu.com/t/oracular-oriole-release-notes/48661
---

# Versiones y Requerimientos
## Ubuntu {{< param "ubuntuVersions.ltsVersion" >}}
Ubuntu {{< param "ubuntuVersions.ltsVersion" >}}, la versión más reciente de soporte a largo plazo (LTS), cuenta con mantenimiento gratuito y actualizaciones de seguridad durante 5 años.
Para la mayoría de los usuarios, se recomienda el uso de la versión LTS para asegurar la estabilidad.

- [Ver notas de lanzamiento de Ubuntu {{< param "ubuntuVersions.ltsVersion" >}}]({{< param "ubuntuVersions.ltsReleaseNote" >}})

## Ubuntu {{< param "ubuntuVersions.normalVersion" >}}
Si deseas probar las funciones más nuevas primero, utiliza la versión más reciente, Ubuntu {{< param "ubuntuVersions.normalVersion" >}}. Se proporcionan actualizaciones de mantenimiento y seguridad gratuitas durante 9 meses después del lanzamiento.

[Ver notas de lanzamiento de Ubuntu {{< param "ubuntuVersions.normalVersion" >}}]({{< param "ubuntuVersions.normalReleaseNote" >}})

## Ciclo de Lanzamiento y Soporte
Ubuntu lanza una nueva versión cada año en abril y octubre, con un intervalo de 6 meses. La versión de soporte a largo plazo (LTS) se lanza cada dos años en abril de los años pares.
Las versiones LTS tienen soporte por 5 años, mientras que las versiones intermedias tienen soporte por 9 meses.

{{< button text="Ciclo de lanzamiento de Ubuntu (Inglés)" href="https://ubuntu.com/about/release-cycle" icon="information" >}}

## Requerimientos del Sistema

 - Procesador de doble núcleo a 2 GHz o superior
 - 4 GB de memoria del sistema (RAM)
 - 25 GB de espacio libre en el disco duro
 - Acceso a Internet (recomendado)
 - Medio de instalación: Unidad de DVD o puerto USB para el instalador

# Descarga

## Descarga desde el Sitio Oficial

{{< button text="Desktop" href="https://ubuntu.com/download/desktop" icon="begin-downloading" >}}
{{< button text="Server" href="https://ubuntu.com/download/server" icon="machines" >}}
{{< button text="Raspberry Pi" href="https://ubuntu.com/download/raspberry-pi" icon="switcher-dashboard" >}}
{{< button text="Internet de las Cosas (Ubuntu Core)" href="https://ubuntu.com/download/iot" icon="switcher-dashboard" >}}

## Espejos (Mirrors) Oficiales
Puedes encontrar una lista completa de espejos oficiales de Ubuntu en todo el mundo, incluyendo opciones en Latinoamérica.

[Ver lista de espejos oficiales en Launchpad.net](https://launchpad.net/ubuntu/+archivemirrors)

# Instalación y Uso

## Desktop y Server
- Desktop: [Guía de instalación (Inglés)](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- Server: [Tutorial de instalación (Inglés)](https://ubuntu.com/tutorials/install-ubuntu-server)
- [Lista de hardware certificado por Ubuntu](https://ubuntu.com/certified)

## Uso en Nube Pública
- [Imágenes para nube pública](http://cloud-images.ubuntu.com/)
- Amazon Web Services: [Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=565feec9-3d43-413e-9760-c651546613f2)
- Microsoft Azure: [Ubuntu en Azure](https://azure.microsoft.com/es-es/explore/ubuntu)
- Google Cloud Platform: [Marketplace](https://console.cloud.google.com/marketplace/product/ubuntu-os-cloud/ubuntu-focal)

## WSL (Windows Subsystem for Linux)
Si estás usando Windows 10 o Windows 11, puedes usar Ubuntu fácilmente a través del entorno WSL.

{{< button text="Instalar Ubuntu en WSL (Documentación oficial)" href="https://learn.microsoft.com/es-es/windows/wsl/install" icon="begin-downloading" >}}

## Contenedores Linux
Imágenes de contenedores para aplicaciones: Docker, Podman, Kubernetes, etc.

{{< button text="Docker Hub" href="https://hub.docker.com/_/ubuntu" icon="begin-downloading" >}}
{{< button text="Amazon ECR Public Gallery" href="https://gallery.ecr.aws/ubuntu/ubuntu" icon="begin-downloading" >}}

# Obtener Ayuda
Si necesitas ayuda mientras usas Ubuntu, puedes obtenerla a través de varios canales y comunidades en línea.

{{< button text="Foro de la Comunidad" href="https://discourse.ubuntu-ve.org/" >}}
{{< button text="Lista de Correo" href="https://lists.ubuntu.com/mailman/listinfo/ubuntu-ve" >}}
{{< button text="Grupo de Telegram" href="https://t.me/ubuntuve" >}}

{{< button text="Ask Ubuntu (Inglés)" href="https://askubuntu.com/" >}}
{{< button text="Foros de Ubuntu (Inglés)" href="https://ubuntuforums.org/" >}}

# Soporte Técnico Comercial

{{< info title="Nota informativa" content="La Comunidad de Ubuntu Venezuela es una comunidad de usuarios y desarrolladores que opera de forma independiente de Canonical Ltd. y sin fines de lucro. No proporcionamos soporte técnico comercial para Ubuntu. Si lo requiere, consulte la información a continuación para recibir soporte de Canonical Ltd. o sus socios." >}}

## Ubuntu Pro
Puedes obtener soporte comercial de Canonical Ltd., los desarrolladores de Ubuntu, a través de Ubuntu Pro.

{{< button text="Ubuntu Pro (Inglés)" href="https://ubuntu.com/pro" icon="information" >}}
