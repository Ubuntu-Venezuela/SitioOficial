import subprocess
import platform
import os
import sys

class WSLManager:
    """Maneja la detección y ejecución de comandos a través de WSL"""
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.wsl_available = False
        self.wsl_distro = None
        self._check_wsl()
    
    def _check_wsl(self):
        """Verifica si WSL está disponible y configurado"""
        if not self.is_windows:
            return
        
        try:
            # Verificar si WSL está instalado
            result = subprocess.run(["wsl", "--list", "--quiet"], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                distros = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                if distros:
                    self.wsl_available = True
                    # Preferir Ubuntu si está disponible
                    ubuntu_distros = [d for d in distros if 'ubuntu' in d.lower()]
                    self.wsl_distro = ubuntu_distros[0] if ubuntu_distros else distros[0]
                    
        except Exception:
            pass
    
    def execute_command(self, command, **kwargs):
        """Ejecuta un comando, usando WSL si estamos en Windows"""
        if self.is_windows and self.wsl_available:
            # Convertir el comando para WSL
            if isinstance(command, list):
                wsl_command = ["wsl", "-d", self.wsl_distro] + command
            else:
                wsl_command = f"wsl -d {self.wsl_distro} {command}"
            
            return subprocess.run(wsl_command, **kwargs)
        else:
            # Ejecutar directamente en Linux o si WSL no está disponible
            return subprocess.run(command, **kwargs)
    
    def get_linux_path(self, windows_path):
        """Convierte una ruta de Windows a una ruta de WSL"""
        if not self.is_windows or not self.wsl_available:
            return windows_path
        
        # Convertir C:\Users\... a /mnt/c/Users/...
        if windows_path.startswith(('C:', 'c:')):
            linux_path = windows_path.replace('C:', '/mnt/c').replace('c:', '/mnt/c')
            linux_path = linux_path.replace('\\', '/')
            return linux_path
        
        return windows_path
    
    def get_home_directory(self):
        """Obtiene el directorio home correcto según el entorno"""
        if self.is_windows and self.wsl_available:
            # Usar el home de WSL
            result = self.execute_command(["echo", "$HOME"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        
        return os.path.expanduser("~")
    
    def check_requirements(self):
        """Verifica que todos los requisitos estén disponibles"""
        if not self.is_windows:
            return True, "Ejecutando en Linux nativo"
        
        if not self.wsl_available:
            return False, self._get_wsl_installation_instructions()
        
        # Verificar que las herramientas necesarias estén instaladas en WSL
        tools = ["gpg", "ssh-keygen", "apt"]
        missing_tools = []
        
        for tool in tools:
            result = self.execute_command(["which", tool], capture_output=True, text=True)
            if result.returncode != 0:
                missing_tools.append(tool)
        
        if missing_tools:
            return False, f"Herramientas faltantes en WSL: {', '.join(missing_tools)}"
        
        return True, f"WSL configurado correctamente con {self.wsl_distro}"
    
    def _get_wsl_installation_instructions(self):
        """Retorna instrucciones para instalar WSL"""
        return """
WSL no está disponible. Para instalar WSL:

1. Abre PowerShell como Administrador
2. Ejecuta: wsl --install
3. Reinicia tu computadora
4. Configura tu usuario de Ubuntu
5. Ejecuta esta aplicación nuevamente

Alternativamente, puedes instalar desde Microsoft Store:
- Busca "Ubuntu" en Microsoft Store
- Instala Ubuntu 20.04 LTS o superior
"""

# Instancia global del manager
wsl_manager = WSLManager()