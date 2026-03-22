import subprocess
import os
from wsl_manager import wsl_manager

def generate_ssh_key():
    """Genera una clave SSH usando WSL si estamos en Windows"""
    
    # Obtener el directorio home correcto
    home_dir = wsl_manager.get_home_directory()
    ssh_dir = f"{home_dir}/.ssh"
    key_path = f"{ssh_dir}/id_rsa"
    
    # Crear directorio .ssh si no existe
    wsl_manager.execute_command(["mkdir", "-p", ssh_dir], check=True)
    
    # Generar la clave SSH
    result = wsl_manager.execute_command([
        "ssh-keygen", "-b", "2048", "-t", "rsa", 
        "-f", key_path, "-N", ""
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Error generando la clave SSH: {result.stderr}")
    
    # Leer la clave pública
    pub_key_path = f"{key_path}.pub"
    cat_result = wsl_manager.execute_command(
        ["cat", pub_key_path], 
        capture_output=True, text=True
    )
    
    if cat_result.returncode != 0:
        raise Exception("No se pudo leer la clave SSH pública generada.")
    
    ssh_key = cat_result.stdout.strip()
    
    # Configurar permisos correctos
    wsl_manager.execute_command(["chmod", "600", key_path])
    wsl_manager.execute_command(["chmod", "644", pub_key_path])
    
    return ssh_key
