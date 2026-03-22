#!/usr/bin/env python3
"""
Setup script for Ubuntu Code of Conduct Tool
Supports both Windows (with WSL) and Linux environments
"""

import subprocess
import sys
import os
import platform

def check_python():
    """Check if Python is properly installed"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 o superior es requerido")
        return False
    print(f"✓ Python {sys.version.split()[0]} detectado")
    return True

def check_wsl():
    """Check if WSL is available on Windows"""
    if platform.system() != "Windows":
        return True, "Linux nativo"
    
    try:
        result = subprocess.run(["wsl", "--list", "--quiet"], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            distros = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            if distros:
                ubuntu_distros = [d for d in distros if 'ubuntu' in d.lower()]
                distro = ubuntu_distros[0] if ubuntu_distros else distros[0]
                return True, f"WSL disponible ({distro})"
        
        return False, "WSL no está instalado"
        
    except Exception:
        return False, "WSL no está disponible"

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Instalando dependencias de Python...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, shell=True)
        print("✓ Dependencias de Python instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def install_streamlit_if_missing():
    """Install Streamlit if not available"""
    try:
        import streamlit
        print("✓ Streamlit ya está instalado")
        return True
    except ImportError:
        print("📦 Instalando Streamlit...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], 
                          check=True, shell=True)
            print("✓ Streamlit instalado")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando Streamlit")
            return False

def run_app():
    """Run the Streamlit application"""
    try:
        print("\n🚀 Iniciando Ubuntu Code of Conduct Tool...")
        print("La aplicación se abrirá en tu navegador web.")
        print("Presiona Ctrl+C para detener la aplicación.")
        print("=" * 50)
        
        # Change to the correct directory
        app_path = os.path.join(os.path.dirname(__file__), "ui", "app.py")
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], 
                      shell=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")

def show_wsl_instructions():
    """Show WSL installation instructions"""
    print("""
🔧 INSTRUCCIONES PARA INSTALAR WSL
================================

Para usar esta herramienta en Windows, necesitas WSL:

1. 📋 Abre PowerShell como Administrador:
   - Presiona Win + X
   - Selecciona "Windows PowerShell (Administrador)"

2. 🔽 Instala WSL:
   wsl --install

3. 🔄 Reinicia tu computadora cuando se solicite

4. 🐧 Configura Ubuntu:
   - Se abrirá automáticamente después del reinicio
   - Crea un usuario y contraseña para Ubuntu

5. ✅ Ejecuta este script nuevamente

Alternativamente, puedes instalar desde Microsoft Store:
- Busca "Ubuntu" en Microsoft Store
- Instala "Ubuntu 20.04 LTS" o superior

Para más información: https://docs.microsoft.com/en-us/windows/wsl/install
""")

def main():
    print("🔧 Ubuntu Code of Conduct Tool - Setup")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        return
    
    # Check WSL on Windows
    wsl_available, wsl_message = check_wsl()
    print(f"🐧 Entorno: {wsl_message}")
    
    if not wsl_available:
        show_wsl_instructions()
        return
    
    # Install Python dependencies
    if not install_requirements():
        return
    
    # Ensure Streamlit is available
    if not install_streamlit_if_missing():
        return
    
    print("\n✅ Setup completado exitosamente!")
    
    # Show environment info
    if platform.system() == "Windows":
        print("""
💡 INFORMACIÓN IMPORTANTE PARA WINDOWS:
- Esta herramienta usa WSL para mantener compatibilidad completa
- Las claves se generan en el entorno Linux de WSL
- Son accesibles tanto desde Windows como desde WSL
""")
    
    response = input("\n¿Quieres ejecutar la aplicación ahora? (s/n): ")
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        run_app()
    else:
        print(f"""
Para ejecutar la aplicación más tarde, usa:
python setup.py

O directamente:
streamlit run ui/app.py
""")

if __name__ == "__main__":
    main()