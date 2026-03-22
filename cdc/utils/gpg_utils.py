import subprocess
import tempfile
import os
from wsl_manager import wsl_manager

def generate_gpg_key(nombre, apellido, correo, key_size="2048 bits"):
    """Genera una clave GPG usando WSL si estamos en Windows"""
    
    # Extraer el valor numérico del tamaño de clave
    key_length = key_size.split()[0]
    
    genkey_content = f"""Key-Type: 1
Key-Length: {key_length}
Subkey-Type: 1
Subkey-Length: {key_length}
Name-Real: {nombre} {apellido}
Name-Email: {correo}
Expire-Date: 2y
%commit
%echo done"""

    # Crear archivo temporal
    if wsl_manager.is_windows and wsl_manager.wsl_available:
        # En WSL, usar /tmp
        temp_file = "/tmp/genkey_ubuntucdc"
        # Escribir el archivo usando WSL
        echo_command = f'echo "{genkey_content}" > {temp_file}'
        wsl_manager.execute_command(["bash", "-c", echo_command], check=True)
    else:
        # En Linux nativo
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(genkey_content)
            temp_file = f.name

    try:
        # Generar la clave GPG
        result = wsl_manager.execute_command(
            ["gpg", "--batch", "--gen-key", temp_file], 
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Error generando la llave GPG: {result.stderr}")

        # Obtener el ID de la clave
        list_result = wsl_manager.execute_command(
            ["gpg", "--list-secret-keys", "--keyid-format", "LONG", correo], 
            capture_output=True, text=True
        )
        
        if list_result.returncode != 0:
            raise Exception(f"Error listando las claves: {list_result.stderr}")
        
        # Extraer el ID de la clave
        lines = list_result.stdout.splitlines()
        millave = None
        for line in lines:
            if "sec" in line and "/" in line:
                millave = line.split("/")[1].split()[0]
                break
        
        if not millave:
            raise Exception("No se pudo extraer la clave GPG generada.")

        # Obtener la huella digital
        fingerprint_result = wsl_manager.execute_command(
            ["gpg", "--fingerprint", millave], 
            capture_output=True, text=True
        )
        
        mihuella = millave  # Por defecto usar el ID
        if fingerprint_result.returncode == 0:
            for line in fingerprint_result.stdout.splitlines():
                if "Key fingerprint" in line or "Huella" in line:
                    # Extraer la huella digital
                    if "=" in line:
                        mihuella = line.split("=")[-1].strip().replace(" ", "")
                    break

        # Enviar la clave al servidor de claves (opcional)
        try:
            wsl_manager.execute_command(
                ["gpg", "--send-keys", "--keyserver", "keyserver.ubuntu.com", millave],
                capture_output=True, text=True, timeout=30
            )
        except:
            # No es crítico si falla el envío al servidor
            pass

        return millave, mihuella
        
    finally:
        # Limpiar archivo temporal
        try:
            if wsl_manager.is_windows and wsl_manager.wsl_available:
                wsl_manager.execute_command(["rm", "-f", temp_file])
            else:
                os.unlink(temp_file)
        except:
            pass
