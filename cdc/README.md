# Ubuntu Code of Conduct Tool

Herramienta web moderna para la generación de claves GPG y SSH para la firma del código de conducta de Ubuntu.

Este proyecto es un **feature adicional** al proyecto original [cocsign](https://github.com/Ubuntu-Venezuela/cocsign/) que proporciona una interfaz web intuitiva y documentación completa para usuarios de Windows con WSL y Linux nativo.

## Proyecto Original: cocsign

Script para la firma del código de conducta de ubuntu

Basado en código de Eduardo Echeverria <echevemaster@gmail.com>

### Modificaciones / Correcciones / Optimizaciones

* Hector Mantellini <xombra.com@gmail.com>
* Jesus Palencia

### Uso del script original:

```bash
cocsign instalar|iniciar nombre apellido tu@correo.com
```

Repositorio original: https://github.com/Ubuntu-Venezuela/cocsign/

## Nuevo Feature: Interfaz Web

Esta herramienta web moderna complementa el script original cocsign proporcionando:

* Interfaz gráfica intuitiva con Streamlit
* Compatibilidad completa con Windows WSL y Linux nativo
* Documentación interactiva paso a paso
* Generación automática de claves GPG y SSH
* Guías específicas para cada sistema operativo

## Características

### Funcionalidades Principales

* **Detección automática del entorno**: Identifica si se ejecuta en Windows con WSL o Linux nativo
* **Generación de claves GPG**: Soporte para múltiples tamaños de clave (1024, 2048, 3072, 4096 bits)
* **Generación de claves SSH**: Creación automática de claves SSH para autenticación
* **Instalación de dependencias**: Verificación e instalación automática de herramientas necesarias
* **Interfaz moderna**: Diseño responsive con colores oficiales de Ubuntu

### Compatibilidad

* **Windows 10/11** con WSL (Windows Subsystem for Linux)
* **Linux nativo** (Ubuntu, Debian, y derivados)
* **Distribuciones WSL soportadas**: Ubuntu, Debian

## Instalación

### Requisitos Previos

#### Para Windows:
1. **Instalar WSL**:
   ```powershell
   # Ejecutar en PowerShell como Administrador
   wsl --install
   ```
2. Reiniciar el sistema
3. Configurar Ubuntu en WSL

#### Para Linux:
```bash
# Instalar Python y pip
sudo apt update
sudo apt install python3 python3-pip

# Verificar herramientas
gpg --version
ssh -V
```

### Instalación de la Aplicación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Ubuntu-Venezuela/CDC.git
   cd CDC
   ```

2. **Instalar dependencias Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   streamlit run ui/app.py
   ```

4. **Abrir en el navegador**:
   ```
   http://localhost:8501
   ```

## Uso

### Interfaz Web

La aplicación cuenta con dos pestañas principales:

#### 1. Generador de Claves

1. **Verificar dependencias**: Marcar la opción y hacer clic en "Instalar"
2. **Introducir datos personales**:
   * Nombre
   * Apellido
   * Correo electrónico
3. **Seleccionar tamaño de clave GPG** (recomendado: 2048 bits o superior)
4. **Generar claves**: Hacer clic en "Generar Claves"
5. **Seguir instrucciones post-generación**

#### 2. Documentación

Documentación completa con:
* Guía específica para Windows + WSL
* Guía específica para Linux nativo
* Preguntas frecuentes (FAQ)
* Solución de problemas
* Mejores prácticas de seguridad

### Configuración Post-Generación

#### Para Windows con WSL:
```bash
# Configurar Git para usar WSL GPG
git config --global gpg.program "wsl gpg"
git config --global user.signingkey TU_CLAVE_GPG
git config --global commit.gpgsign true

# Agregar clave SSH
wsl ssh-add ~/.ssh/id_rsa
```

#### Para Linux nativo:
```bash
# Configurar Git
git config --global user.signingkey TU_CLAVE_GPG
git config --global commit.gpgsign true

# Iniciar agente SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

## Estructura del Proyecto

```
ubuntucdc/
├── ui/
│   └── app.py              # Interfaz principal de Streamlit
├── utils/
│   ├── gpg_utils.py        # Utilidades para GPG
│   ├── ssh_utils.py        # Utilidades para SSH
│   ├── install_utils.py    # Instalación de dependencias
│   └── wsl_manager.py      # Gestión de WSL/Linux
├── scripts/
│   └── install.sh          # Script de instalación
├── requirements.txt        # Dependencias Python
├── setup.py               # Configuración del proyecto
└── README.md              # Este archivo
```

## Comandos Útiles

### Gestión de Claves GPG

```bash
# Listar claves privadas
gpg --list-secret-keys --keyid-format LONG

# Exportar clave pública
gpg --armor --export CLAVE_ID

# Enviar clave a servidor
gpg --send-keys CLAVE_ID

# Firmar commit
git commit -S -m "Mensaje del commit"
```

### Gestión de Claves SSH

```bash
# Probar conexión SSH con GitHub
ssh -T git@github.com

# Copiar clave pública
cat ~/.ssh/id_rsa.pub

# Agregar clave al agente
ssh-add ~/.ssh/id_rsa
```

## Solución de Problemas

### Windows WSL

**WSL no funciona**:
```powershell
# Actualizar WSL
wsl --update

# Verificar versión
wsl --version

# Listar distribuciones
wsl --list --verbose
```

**Problemas con GPG**:
```bash
# Reiniciar agente GPG
wsl gpgconf --kill gpg-agent

# Verificar instalación
wsl gpg --version
```

### Linux

**Dependencias faltantes**:
```bash
# Instalar herramientas necesarias
sudo apt install gnupg openssh-client wget curl

# Verificar instalación
gpg --version && ssh -V
```

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Autores y Reconocimientos

### Proyecto Original (cocsign)
* **Eduardo Echeverria** <echevemaster@gmail.com> - Código base
* **Hector Mantellini** <xombra.com@gmail.com> - Modificaciones y optimizaciones
* **Jesus Palencia** - Correcciones

### Feature Web Interface
* **Desarrollo de la interfaz web moderna**
* **Documentación completa**
* **Compatibilidad Windows WSL/Linux**
* **Mejoras de UX/UI**

## Licencia

Este proyecto mantiene la misma licencia que el proyecto original cocsign.

## Enlaces

* **Repositorio original cocsign**: https://github.com/Ubuntu-Venezuela/cocsign/
* **Repositorio actual**: https://github.com/Ubuntu-Venezuela/CDC
* **Ubuntu Code of Conduct**: https://ubuntu.com/community/code-of-conduct
* **Documentación WSL**: https://docs.microsoft.com/en-us/windows/wsl/

## Estado del Proyecto

Proyecto activo en desarrollo. Se aceptan contribuciones y sugerencias.

### Próximas Funcionalidades

* Exportación automática de claves
* Integración con servicios de claves
* Soporte para más tipos de claves
* Interfaz en múltiples idiomas
* Modo offline completo
