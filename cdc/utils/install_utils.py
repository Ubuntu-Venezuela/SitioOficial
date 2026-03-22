import subprocess
import sys
import os
from wsl_manager import wsl_manager

def install_dependencies():
    """
    Instala las dependencias necesarias usando WSL si estamos en Windows,
    o directamente en Linux si estamos en un entorno nativo.
    """
    
    # Verificar que WSL esté disponible si estamos en Windows
    is_available, message = wsl_manager.check_requirements()
    if not is_available:
        raise Exception(message)
    
    try:
        print("🔍 Verificando dependencias del sistema...")
        
        # Actualizar repositorios
        print("📦 Actualizando repositorios...")
        update_result = wsl_manager.execute_command(
            ["sudo", "apt", "update"], 
            capture_output=True, text=True
        )
        
        if update_result.returncode != 0:
            print("⚠️  Advertencia: No se pudieron actualizar los repositorios")
            print(f"Error: {update_result.stderr}")
        
        # Lista de paquetes necesarios
        packages = ["gnupg", "openssh-client", "wget", "curl"]
        
        print("🔧 Instalando dependencias...")
        for package in packages:
            print(f"   - Instalando {package}...")
            install_result = wsl_manager.execute_command(
                ["sudo", "apt", "install", "-y", package],
                capture_output=True, text=True
            )
            
            if install_result.returncode != 0:
                print(f"⚠️  Advertencia: No se pudo instalar {package}")
                print(f"Error: {install_result.stderr}")
        
        # Verificar que las herramientas estén disponibles
        tools_status = {}
        tools = {
            "gpg": "GPG para firmas digitales",
            "ssh-keygen": "SSH para claves de autenticación", 
            "wget": "Descarga de archivos",
            "curl": "Transferencia de datos"
        }
        
        print("\n✅ Verificando instalación...")
        all_ok = True
        
        for tool, description in tools.items():
            result = wsl_manager.execute_command(
                ["which", tool], 
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print(f"   ✓ {tool}: {description}")
                tools_status[tool] = True
            else:
                print(f"   ❌ {tool}: No disponible")
                tools_status[tool] = False
                all_ok = False
        
        if all_ok:
            print("\n🎉 ¡Todas las dependencias están instaladas correctamente!")
            
            # Mostrar información del entorno
            if wsl_manager.is_windows:
                print(f"🐧 Entorno: WSL ({wsl_manager.wsl_distro})")
            else:
                print("🐧 Entorno: Linux nativo")
                
            return True
        else:
            missing = [tool for tool, status in tools_status.items() if not status]
            raise Exception(f"Faltan herramientas: {', '.join(missing)}")
            
    except Exception as e:
        if "sudo" in str(e):
            raise Exception(
                "Se requieren permisos de administrador. "
                "Asegúrate de que tu usuario tenga permisos sudo en WSL."
            )
        else:
            raise Exception(f"Error durante la instalación: {str(e)}")

def check_environment():
    """Verifica el entorno y muestra información útil"""
    
    print("🔍 Información del entorno:")
    print("=" * 40)
    
    if wsl_manager.is_windows:
        if wsl_manager.wsl_available:
            print(f"💻 Sistema: Windows con WSL")
            print(f"🐧 Distribución WSL: {wsl_manager.wsl_distro}")
            
            # Verificar versión de Ubuntu en WSL
            version_result = wsl_manager.execute_command(
                ["lsb_release", "-d"], 
                capture_output=True, text=True
            )
            if version_result.returncode == 0:
                print(f"📋 Versión: {version_result.stdout.strip()}")
        else:
            print("💻 Sistema: Windows (WSL no disponible)")
            print("⚠️  Se requiere WSL para funcionalidad completa")
    else:
        print("💻 Sistema: Linux nativo")
        
        # Mostrar información del sistema
        try:
            version_result = subprocess.run(
                ["lsb_release", "-d"], 
                capture_output=True, text=True
            )
            if version_result.returncode == 0:
                print(f"📋 Versión: {version_result.stdout.strip()}")
        except:
            pass
    
    print("=" * 40)
