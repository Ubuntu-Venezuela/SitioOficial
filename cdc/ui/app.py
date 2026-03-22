import streamlit as st
import sys
import os

# Añadir el directorio utils al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from gpg_utils import generate_gpg_key
from ssh_utils import generate_ssh_key
from install_utils import install_dependencies, check_environment
from wsl_manager import wsl_manager

HOME = os.path.expanduser("~")

# Colores oficiales de Ubuntu
UBUNTU_ORANGE = "#E95420"
UBUNTU_LIGHT_ORANGE = "#EF7627"
UBUNTU_DARK_ORANGE = "#C7491D"
UBUNTU_GREY = "#333333"
UBUNTU_LIGHT_GREY = "#888888"
UBUNTU_WHITE = "#FFFFFF"
UBUNTU_BLACK = "#000000"

# Estilos CSS para Streamlit
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {UBUNTU_WHITE};
        color: {UBUNTU_GREY};
    }}
    
    /* Contenedor principal centrado */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* Remover márgenes laterales de Streamlit */
    .css-1d391kg, .css-18e3th9, .css-1lcbmhc {{
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    
    .css-12oz5g7 {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    
    /* Título principal */
    h1 {{
        color: {UBUNTU_ORANGE} !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-weight: 600 !important;
        width: 100%;
    }}
    
    h3 {{
        color: {UBUNTU_GREY} !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }}
    
    /* Botones */
    .stButton>button {{
        background-color: {UBUNTU_ORANGE};
        color: {UBUNTU_WHITE};
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {UBUNTU_LIGHT_ORANGE};
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(233, 84, 32, 0.3);
    }}
    
    /* Inputs de texto */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {UBUNTU_WHITE};
        color: {UBUNTU_GREY};
        border-color: {UBUNTU_LIGHT_GREY};
        border-width: 2px;
        border-style: solid;
        border-radius: 6px;
        padding: 0.5rem;
        font-size: 14px;
        width: 100%;
    }}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {UBUNTU_ORANGE};
        box-shadow: 0 0 0 2px rgba(233, 84, 32, 0.2);
    }}
    
    /* Checkboxes */
    .stCheckbox {{
        margin: 0.25rem 0;
    }}
    .stCheckbox > label {{
        display: flex;
        align-items: center;
        font-size: 14px;
        color: {UBUNTU_GREY};
    }}
    
    /* Selectbox */
    .stSelectbox>div>div>div {{
        background-color: {UBUNTU_WHITE};
        color: {UBUNTU_GREY};
        border-color: {UBUNTU_LIGHT_GREY};
        border-radius: 6px;
    }}
    
    /* Mensajes de estado */
    .stSuccess {{
        background-color: rgba(233, 84, 32, 0.1);
        border: 1px solid {UBUNTU_ORANGE};
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    .stSuccess > div {{
        color: {UBUNTU_DARK_ORANGE} !important;
        font-weight: 500;
    }}
    
    .stInfo {{
        background-color: rgba(239, 118, 39, 0.1);
        border: 1px solid {UBUNTU_LIGHT_ORANGE};
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    .stInfo > div {{
        color: {UBUNTU_LIGHT_ORANGE} !important;
        font-weight: 500;
    }}
    
    .stError {{
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    .stError > div {{
        color: #dc3545 !important;
        font-weight: 500;
    }}
    
    .stWarning {{
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    .stWarning > div {{
        color: #fd7e14 !important;
        font-weight: 500;
    }}
    
    /* Información del entorno */
    .environment-info {{
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {UBUNTU_ORANGE};
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
    }}
    
    /* Columnas centradas */
    .stColumn {{
        padding: 0 0.5rem;
    }}
    
    .stColumn > div {{
        width: 100%;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background-color: {UBUNTU_ORANGE};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: rgba(233, 84, 32, 0.1);
        border-radius: 6px;
        border: 1px solid {UBUNTU_LIGHT_GREY};
    }}
    
    /* Code blocks */
    .stCodeBlock {{
        border-radius: 6px;
        border: 1px solid {UBUNTU_LIGHT_GREY};
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {UBUNTU_ORANGE} !important;
    }}
    
    /* Remover padding lateral del sidebar */
    .css-1d391kg {{
        background-color: {UBUNTU_WHITE};
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    
    /* Footer */
    footer {{
        background-color: {UBUNTU_ORANGE};
        color: {UBUNTU_BLACK};
        padding: 15px 0;
        text-align: center;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        z-index: 999;
        margin: 0;
        box-sizing: border-box;
    }}
    footer p {{
        margin: 5px 0;
        padding: 0;
        color: {UBUNTU_BLACK};
        font-size: 14px;
    }}
    footer a {{
        color: {UBUNTU_BLACK};
        text-decoration: none;
        margin: 0 10px;
        font-weight: 500;
    }}
    footer a:hover {{
        text-decoration: underline;
        color: {UBUNTU_WHITE};
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem 0.5rem;
        }}
        .stColumn {{
            padding: 0 0.25rem;
        }}
    }}
    
    /* Forzar centrado completo */
    .element-container {{
        width: 100% !important;
    }}
    
    .stMarkdown {{
        width: 100% !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Ubuntu Code of Conduct Tool")

# Crear pestañas
tab1, tab2 = st.tabs(["🔧 Generador de Claves", "📚 Documentación"])

with tab1:
    # Mostrar información del entorno
    st.markdown("### 🔍 Información del Entorno")

    if wsl_manager.is_windows:
        if wsl_manager.wsl_available:
            st.markdown(
                f"""
                <div class="environment-info">
                    <strong>💻 Sistema:</strong> Windows con WSL<br>
                    <strong>🐧 Distribución:</strong> {wsl_manager.wsl_distro}<br>
                    <strong>✅ Estado:</strong> Listo para generar claves
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error(
                """
                ⚠️ **WSL no está disponible**
                
                Para usar esta herramienta en Windows, necesitas instalar WSL:
                
                1. Abre PowerShell como Administrador
                2. Ejecuta: `wsl --install`
                3. Reinicia tu computadora
                4. Configura Ubuntu
                5. Vuelve a ejecutar esta aplicación
                """
            )
            st.stop()
    else:
        st.markdown(
            """
            <div class="environment-info">
                <strong>💻 Sistema:</strong> Linux nativo<br>
                <strong>✅ Estado:</strong> Listo para generar claves
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Layout horizontal para botones y guía
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Opciones")

        option = st.checkbox("Instalar/Verificar dependencias")

        if option:
            if st.button("Instalar"):
                try:
                    with st.spinner("Verificando e instalando dependencias..."):
                        install_dependencies()
                    st.success("✅ Dependencias verificadas e instaladas correctamente.")
                except Exception as e:
                    st.error(f"❌ Error durante la instalación: {e}")
        else:
            nombre = st.text_input("Nombre", placeholder="Ej: Juan")
            apellido = st.text_input("Apellido", placeholder="Ej: Pérez")
            correo = st.text_input("Correo", placeholder="Ej: juan.perez@example.com")

            st.markdown("**Selecciona el tamaño de la clave GPG:**")
            key_size_1024 = st.checkbox("1024 bits (Menos seguro, no recomendado)")
            key_size_2048 = st.checkbox("2048 bits (Recomendado)", value=True)
            key_size_3072 = st.checkbox("3072 bits (Mayor seguridad)")
            key_size_4096 = st.checkbox("4096 bits (Muy alta seguridad)")

            key_sizes = []
            if key_size_1024:
                key_sizes.append("1024 bits")
            if key_size_2048:
                key_sizes.append("2048 bits")
            if key_size_3072:
                key_sizes.append("3072 bits")
            if key_size_4096:
                key_sizes.append("4096 bits")

            if st.button("🚀 Generar Claves"):
                if not nombre or not apellido or not correo:
                    st.warning("⚠️ Por favor, complete todos los campos.")
                elif not key_sizes:
                    st.warning("⚠️ Por favor, seleccione al menos un tamaño de clave.")
                else:
                    try:
                        # Verificar dependencias primero
                        is_available, message = wsl_manager.check_requirements()
                        if not is_available:
                            st.error(f"❌ {message}")
                            st.stop()
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Generar claves GPG
                        for i, size in enumerate(key_sizes):
                            status_text.text(f"🔐 Generando clave GPG de {size}...")
                            progress_bar.progress((i + 1) / (len(key_sizes) + 1))
                            
                            millave, mihuella = generate_gpg_key(nombre, apellido, correo, size)
                            st.success(f"✅ Clave GPG generada ({size}): `{millave}`")
                            st.info(f"🔑 Huella digital: `{mihuella}`")

                        # Generar clave SSH
                        status_text.text("🔑 Generando clave SSH...")
                        progress_bar.progress(1.0)
                        
                        ssh_key = generate_ssh_key()
                        st.success("✅ Clave SSH generada correctamente.")
                        
                        # Mostrar la clave SSH en un expander
                        with st.expander("🔍 Ver clave SSH pública"):
                            st.code(ssh_key, language='text')

                        progress_bar.empty()
                        status_text.empty()

                        # Mostrar pasos adicionales
                        st.markdown("### 📋 Instrucciones para Configurar Claves")
                        
                        st.markdown("#### 1. **Importar clave GPG a servidores de claves:**")
                        if wsl_manager.is_windows and wsl_manager.wsl_available:
                            st.code(f"wsl gpg --send-keys {mihuella}", language='bash')
                        else:
                            st.code(f"gpg --send-keys {mihuella}", language='bash')
                        
                        st.markdown("#### 2. **Configurar clave SSH:**")
                        home_dir = wsl_manager.get_home_directory()
                        if wsl_manager.is_windows and wsl_manager.wsl_available:
                            st.code(f"wsl ssh-add {home_dir}/.ssh/id_rsa", language='bash')
                        else:
                            st.code(f"ssh-add {home_dir}/.ssh/id_rsa", language='bash')
                        
                        st.markdown("#### 3. **Configurar cliente de correo:**")
                        st.markdown("""
                        - **Thunderbird**: `Preferencias > Seguridad > Configurar Firma y Cifrado`
                        - **Outlook**: `Archivo > Opciones > Centro de Confianza > Seguridad de Correo Electrónico`
                        - **Evolution**: `Editar > Preferencias > Cuentas de Correo > Seguridad`
                        """)

                    except Exception as e:
                        st.error(f"❌ Error durante el proceso: {e}")
                        
                        # Mostrar información adicional para debugging
                        if wsl_manager.is_windows:
                            st.info("""
                            💡 **Consejos para solucionar problemas:**
                            - Asegúrate de que WSL esté correctamente instalado
                            - Verifica que tengas permisos sudo en WSL
                            - Intenta ejecutar `wsl --update` en PowerShell
                            """)

    with col2:
        st.markdown("### 📖 Guía Rápida")
        
        if wsl_manager.is_windows and wsl_manager.wsl_available:
            st.info(f"🐧 Ejecutando en WSL: {wsl_manager.wsl_distro}")
        
        st.markdown("""
        #### 🔧 **Preparación**
        1. **Verificar Dependencias**: Marca la opción "Instalar/Verificar dependencias" y haz clic en "Instalar".
        
        #### 👤 **Configuración Personal**
        2. **Datos Personales**: Introduce tu nombre, apellido y correo electrónico.
        3. **Tamaño de Clave**: Selecciona el tamaño de las claves GPG (se recomienda 2048 bits o superior).
        
        #### 🚀 **Generación**
        4. **Generar Claves**: Haz clic en "Generar Claves" para crear tus claves GPG y SSH.
        5. **Seguir Instrucciones**: Una vez generadas, sigue las instrucciones adicionales.
        
        #### 🔐 **Uso de las Claves**
        - **GPG**: Para firmar commits, correos electrónicos y documentos
        - **SSH**: Para autenticación segura en servidores y repositorios Git
        """)
        
        if wsl_manager.is_windows:
            st.markdown("""
            #### 💻 **Información para Windows**
            Esta herramienta usa WSL para mantener compatibilidad completa con Ubuntu.
            """)

with tab2:
    st.markdown("# 📚 Documentación Completa")
    
    # Crear sub-pestañas para diferentes sistemas
    doc_tab1, doc_tab2, doc_tab3 = st.tabs(["🪟 Windows + WSL", "🐧 Linux Nativo", "❓ FAQ"])
    
    with doc_tab1:
        st.markdown("## 💻 Guía para Windows con WSL")
        
        st.markdown("### 🔧 Requisitos Previos")
        st.markdown("""
        Antes de usar esta herramienta en Windows, necesitas tener WSL instalado y configurado:
        
        #### 1. **Instalar WSL**
        ```powershell
        # Ejecutar en PowerShell como Administrador
        wsl --install
        ```
        
        #### 2. **Reiniciar el sistema**
        Después de la instalación, reinicia tu computadora.
        
        #### 3. **Configurar Ubuntu**
        - Al reiniciar, se abrirá automáticamente la terminal de Ubuntu
        - Crea un usuario y contraseña para Ubuntu
        - Actualiza el sistema:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```
        """)
        
        st.markdown("### 🚀 Uso de la Herramienta")
        st.markdown("""
        #### **Paso 1: Verificar el Entorno**
        - La herramienta detectará automáticamente que estás en Windows con WSL
        - Verás información sobre tu distribución de WSL en la parte superior
        
        #### **Paso 2: Instalar Dependencias**
        1. Marca la casilla "Instalar/Verificar dependencias"
        2. Haz clic en "Instalar"
        3. La herramienta instalará automáticamente:
           - `gnupg` (para claves GPG)
           - `openssh-client` (para claves SSH)
           - `wget` y `curl` (herramientas auxiliares)
        
        #### **Paso 3: Generar Claves**
        1. Introduce tus datos personales:
           - **Nombre**: Tu nombre real
           - **Apellido**: Tu apellido
           - **Correo**: Tu dirección de correo electrónico
        
        2. Selecciona el tamaño de clave GPG:
           - **2048 bits**: Recomendado para uso general
           - **3072 bits**: Mayor seguridad
           - **4096 bits**: Máxima seguridad (más lento)
        
        3. Haz clic en "🚀 Generar Claves"
        """)
        
        st.markdown("### 🔑 Configuración Post-Generación")
        st.markdown("""
        #### **Configurar Git en Windows**
        ```bash
        # Configurar Git para usar WSL GPG
        git config --global gpg.program "wsl gpg"
        git config --global user.signingkey TU_CLAVE_GPG
        git config --global commit.gpgsign true
        ```
        
        #### **Usar SSH desde Windows**
        ```bash
        # Copiar clave SSH pública al portapapeles
        wsl cat ~/.ssh/id_rsa.pub | clip.exe
        
        # Agregar clave SSH al agente
        wsl ssh-add ~/.ssh/id_rsa
        ```
        
        #### **Configurar VS Code**
        ```json
        // En settings.json
        {
            "git.enableCommitSigning": true,
            "terminal.integrated.defaultProfile.windows": "Ubuntu (WSL)"
        }
        ```
        """)
        
        st.markdown("### 🔧 Solución de Problemas")
        st.markdown("""
        #### **WSL no funciona**
        ```powershell
        # Actualizar WSL
        wsl --update
        
        # Verificar versión
        wsl --version
        
        # Listar distribuciones
        wsl --list --verbose
        ```
        
        #### **Problemas con GPG**
        ```bash
        # Verificar instalación
        wsl gpg --version
        
        # Listar claves
        wsl gpg --list-secret-keys
        
        # Reiniciar agente GPG
        wsl gpgconf --kill gpg-agent
        ```
        
        #### **Problemas con SSH**
        ```bash
        # Verificar servicio SSH
        wsl sudo service ssh status
        
        # Iniciar servicio SSH
        wsl sudo service ssh start
        
        # Verificar claves SSH
        wsl ls -la ~/.ssh/
        ```
        """)
    
    with doc_tab2:
        st.markdown("## 🐧 Guía para Linux Nativo")
        
        st.markdown("### 🔧 Requisitos Previos")
        st.markdown("""
        En sistemas Linux nativos (Ubuntu, Debian, etc.), la mayoría de herramientas ya están disponibles:
        
        #### **Verificar herramientas instaladas**
        ```bash
        # Verificar GPG
        gpg --version
        
        # Verificar SSH
        ssh -V
        
        # Verificar Python
        python3 --version
        ```
        """)
        
        st.markdown("### 🚀 Uso de la Herramienta")
        st.markdown("""
        #### **Paso 1: Instalar Dependencias Python**
        ```bash
        # Instalar pip si no está disponible
        sudo apt update
        sudo apt install python3-pip
        
        # Instalar dependencias de la aplicación
        pip3 install streamlit python-gnupg cryptography paramiko
        ```
        
        #### **Paso 2: Ejecutar la Aplicación**
        ```bash
        # Navegar al directorio de la aplicación
        cd /ruta/a/ubuntucdc
        
        # Ejecutar Streamlit
        streamlit run ui/app.py
        ```
        
        #### **Paso 3: Usar la Interfaz**
        - La aplicación detectará automáticamente que estás en Linux nativo
        - Sigue los mismos pasos que en Windows para generar claves
        """)
        
        st.markdown("### 🔑 Configuración en Linux")
        st.markdown("""
        #### **Configurar Git**
        ```bash
        # Configurar información personal
        git config --global user.name "Tu Nombre"
        git config --global user.email "tu@email.com"
        
        # Configurar firma GPG
        git config --global user.signingkey TU_CLAVE_GPG
        git config --global commit.gpgsign true
        ```
        
        #### **Configurar SSH**
        ```bash
        # Iniciar agente SSH
        eval "$(ssh-agent -s)"
        
        # Agregar clave SSH
        ssh-add ~/.ssh/id_rsa
        
        # Copiar clave pública
        cat ~/.ssh/id_rsa.pub
        ```
        
        #### **Configurar GPG**
        ```bash
        # Exportar clave pública
        gpg --armor --export TU_CLAVE_GPG
        
        # Enviar a servidor de claves
        gpg --send-keys TU_CLAVE_GPG
        
        # Configurar agente GPG
        echo 'use-agent' >> ~/.gnupg/gpg.conf
        ```
        """)
        
        st.markdown("### 🔧 Comandos Útiles")
        st.markdown("""
        #### **Gestión de Claves GPG**
        ```bash
        # Listar claves privadas
        gpg --list-secret-keys --keyid-format LONG
        
        # Exportar clave pública
        gpg --armor --export CLAVE_ID
        
        # Importar clave
        gpg --import clave.asc
        
        # Firmar un archivo
        gpg --sign archivo.txt
        
        # Verificar firma
        gpg --verify archivo.txt.gpg
        ```
        
        #### **Gestión de Claves SSH**
        ```bash
        # Generar nueva clave SSH
        ssh-keygen -t rsa -b 4096 -C "tu@email.com"
        
        # Cambiar passphrase
        ssh-keygen -p -f ~/.ssh/id_rsa
        
        # Probar conexión SSH
        ssh -T git@github.com
        
        # Agregar clave a servidor remoto
        ssh-copy-id usuario@servidor.com
        ```
        """)
    
    with doc_tab3:
        st.markdown("## ❓ Preguntas Frecuentes")
        
        with st.expander("🔐 ¿Qué diferencia hay entre claves GPG y SSH?"):
            st.markdown("""
            **Claves GPG (GNU Privacy Guard):**
            - Se usan para **firmar y cifrar** datos
            - Ideales para firmar commits de Git, correos electrónicos y documentos
            - Proporcionan **autenticidad** e **integridad**
            - Pueden tener múltiples identidades asociadas
            
            **Claves SSH (Secure Shell):**
            - Se usan para **autenticación** en conexiones remotas
            - Ideales para conectarse a servidores, GitHub, GitLab, etc.
            - Proporcionan acceso seguro sin contraseñas
            - Una clave por conexión/servicio
            """)
        
        with st.expander("🔢 ¿Qué tamaño de clave debo elegir?"):
            st.markdown("""
            **1024 bits:** ❌ **No recomendado** - Considerado inseguro
            
            **2048 bits:** ✅ **Recomendado** - Buen balance entre seguridad y rendimiento
            
            **3072 bits:** ✅ **Mayor seguridad** - Para datos muy sensibles
            
            **4096 bits:** ✅ **Máxima seguridad** - Para máxima protección (más lento)
            
            **Recomendación:** Usa 2048 bits para uso general, 4096 bits para datos críticos.
            """)
        
        with st.expander("🪟 ¿Por qué usar WSL en Windows?"):
            st.markdown("""
            **Ventajas de WSL:**
            - **Compatibilidad completa** con herramientas de Linux
            - **Mismo entorno** que Ubuntu nativo
            - **Integración** con Windows
            - **Rendimiento** casi nativo
            
            **Sin WSL tendrías que:**
            - Usar herramientas diferentes (PuTTY, WinGPG)
            - Configuraciones más complejas
            - Menor compatibilidad con proyectos Linux
            """)
        
        with st.expander("🔧 ¿Cómo verifico que mis claves funcionan?"):
            st.markdown("""
            **Para GPG:**
            ```bash
            # Listar claves
            gpg --list-secret-keys
            
            # Probar firma
            echo "test" | gpg --clearsign
            
            # Verificar en Git
            git commit -S -m "Commit firmado"
            ```
            
            **Para SSH:**
            ```bash
            # Probar conexión a GitHub
            ssh -T git@github.com
            
            # Probar conexión a servidor
            ssh usuario@servidor.com
            
            # Verificar agente SSH
            ssh-add -l
            ```
            """)
        
        with st.expander("🔄 ¿Cómo actualizo o cambio mis claves?"):
            st.markdown("""
            **Renovar clave GPG:**
            ```bash
            # Extender expiración
            gpg --edit-key TU_CLAVE_ID
            # Luego: expire, 2y, save
            
            # Generar nueva subclave
            gpg --edit-key TU_CLAVE_ID
            # Luego: addkey
            ```
            
            **Cambiar clave SSH:**
            ```bash
            # Generar nueva clave
            ssh-keygen -t rsa -b 4096 -f ~/.ssh/nueva_clave
            
            # Actualizar en servicios (GitHub, servidores)
            cat ~/.ssh/nueva_clave.pub
            ```
            """)
        
        with st.expander("🛡️ ¿Cómo mantengo mis claves seguras?"):
            st.markdown("""
            **Mejores prácticas:**
            
            1. **Usa passphrases fuertes** para proteger tus claves privadas
            2. **Haz copias de seguridad** de tus claves en un lugar seguro
            3. **Revoca claves comprometidas** inmediatamente
            4. **Usa fechas de expiración** para claves GPG
            5. **No compartas** nunca tus claves privadas
            
            **Backup de claves:**
            ```bash
            # Exportar clave GPG privada
            gpg --export-secret-keys TU_CLAVE_ID > clave_privada.asc
            
            # Copiar claves SSH
            cp ~/.ssh/id_rsa ~/backup/
            cp ~/.ssh/id_rsa.pub ~/backup/
            ```
            """)

st.markdown("---")

# Footer
st.markdown(
    """
    <footer>
    <p>Ubuntu Code of conduct Tool - Generación segura de claves GPG y SSH</p>
        <p>
            <a href="https://ubuntu.com/community/code-of-conduct" target="_blank">Código de Conducta Ubuntu</a> |
            <a href="https://help.ubuntu.com/community/GnuPrivacyGuardHowto" target="_blank">Guía GPG</a> |
            <a href="https://help.ubuntu.com/community/SSH" target="_blank">Guía SSH</a>
        </p>
    </footer>
    """,
    unsafe_allow_html=True
)
