---
title: "Download Ubuntu"
description: "Get the latest version of Ubuntu and install it on various environments."
image: "download.svg"
backgroundType: suru #light, dark, accent, suru, suru-topped, image
ubuntuVersions:
    ltsVersion: "24.04 LTS"
    normalVersion: "24.10"
    ltsReleaseNote: https://discourse.ubuntu.com/t/noble-numbat-release-notes/44072
    normalReleaseNote: https://discourse.ubuntu.com/t/oracular-oriole-release-notes/48661

---

# Version and system requirements
## Ubuntu {{< param "ubuntuVersions.ltsVersion" >}}
Ubuntu {{< param "ubuntuVersions.ltsVersion" >}}, the latest LTS (Long term support) version provides 5 years of maintenance and security updates for free.
In most cases, the LTS version is recommended for stable use.

- [See Ubuntu {{< param "ubuntuVersions.ltsVersion" >}} release notes]({{< param "ubuntuVersions.ltsReleaseNote" >}})

## Ubuntu {{< param "ubuntuVersions.normalVersion" >}}
If you want to try out the latest features, try out Ubuntu {{< param "ubuntuVersions.normalVersion" >}}, the latest version. It provides 9 months of maintenance and security updates for free.

[See Ubuntu {{< param "ubuntuVersions.normalVersion" >}} release notes]({{< param "ubuntuVersions.normalReleaseNote" >}})

## Ubuntu release and support cycle
A new version of Ubuntu is released every April and October with a 6-month interval. And a new LTS version is released in April of even years with a 2-year interval.
Free maintenance and security updates are provided for 5 years for the LTS version and 9 months for interim releases.
You may check out Ubuntu release cycle information on ubuntu.com

{{< button text="Ubuntu release cycle" href="https://ubuntu.com/about/release-cycle" icon="information" >}}

## System requirements

 - 2 GHz dual-core processor and 4 GB system memory or better
 - 25 GB of free hard drive space
 - Internet access is helpful
 - Either a DVD drive or a USB port for the installer media

# Download

## From the official website

{{< button text="Desktop" href="https://ubuntu.com/download/desktop" icon="begin-downloading" >}}
{{< button text="Server" href="https://ubuntu.com/download/server" icon="machines" >}}
{{< button text="Raspberry Pi" href="https://ubuntu.com/download/raspberry-pi" icon="switcher-dashboard" >}}
{{< button text="Internet of Things (Ubuntu Core)" href="https://ubuntu.com/download/iot" icon="switcher-dashboard" >}}

# How to install and use

## Desktop & Server
- Desktop: [Installation tutorial](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- Server: [Installation tutorial](https://ubuntu.com/tutorials/install-ubuntu-server)
- [List of Certified Ubuntu hardware](https://ubuntu.com/certified)

## Use on Public Clouds
- [Public cloud images](http://cloud-images.ubuntu.com/)
- Amazon Web Services: [Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=565feec9-3d43-413e-9760-c651546613f2)
- Microsoft Azure: [Ubuntu on Azure](https://azure.microsoft.com/en-us/explore/ubuntu)
- Google Cloud Platform: [Marketplace](https://console.cloud.google.com/marketplace/product/ubuntu-os-cloud/ubuntu-focal)

## WSL (Windows Subsystem for Linux)
If you are using the latest version of Windows 10 or Windows 11, you can easily try out Ubuntu with a WSL environment. 

{{< button text="Install Ubuntu on WSL" href="https://learn.microsoft.com/en-us/windows/wsl/install" icon="begin-downloading" >}}

## Linux Containers
Images for Application Containers: For building OCI images to use with Docker, Podman, Kubernetes.

{{< button text="Docker Hub" href="https://hub.docker.com/_/ubuntu" icon="begin-downloading" >}}
{{< button text="Amazon ECR Public Gallery" href="https://gallery.ecr.aws/ubuntu/ubuntu" icon="begin-downloading" >}}

# Get help
If you need help while using Ubuntu, you can get help through online communities such as forums and online chat.

{{< button text="Forums" href="https://discourse.ubuntu.com/c/locos/" >}}
{{< button text="Mailing List" href="https://lists.ubuntu.com/mailman/listinfo/ubuntu-ve" >}}
{{< button text="Telegram Chat" href="https://t.me/ubuntuve" >}}

{{< button text="Ask Ubuntu" href="https://askubuntu.com/" >}}
{{< button text="Ubuntu Forums" href="https://ubuntuforums.org/" >}}
{{< button text="Launchpad Answers" href="https://answers.launchpad.net/ubuntu" >}}

# Commercial technical support

{{< info title="Note" content="The Ubuntu Venezuela Community is a non-profit community consisting of users and developers and is independent from Canonical Ltd. We do not provide any commercial technical support or answers for related inquiries. If you need commercial support for Ubuntu, check out the information below and get support from Canonical Ltd. or Canonical Partners.">}}

## Ubuntu Pro
Get commercial technical support from Canonical Ltd., the publisher of Ubuntu, with the Ubuntu Pro program.

{{< button text="Ubuntu Pro" href="https://ubuntu.com/pro" icon="information" >}}
