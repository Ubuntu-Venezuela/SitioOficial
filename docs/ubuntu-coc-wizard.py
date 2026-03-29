#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ubuntu Code of Conduct - Asistente de Firma v3.2
Uso: python3 ubuntu-coc-wizard.py
"""

import subprocess, sys, os, threading, webbrowser, time
import urllib.request, urllib.parse, re, platform, shutil, tempfile
from pathlib import Path

SYS        = platform.system()
IS_LINUX   = SYS == "Linux"
IS_MAC     = SYS == "Darwin"
IS_WINDOWS = SYS == "Windows"

def _pip_install(*pkgs):
    cmd = [sys.executable, "-m", "pip", "install", "--quiet"] + list(pkgs)
    if IS_LINUX:
        cmd += ["--break-system-packages"]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def _ensure_flask():
    try:
        import flask
        return True
    except ImportError:
        print("Instalando Flask (solo la primera vez)...")
        if _pip_install("flask"):
            return True
        print("No se pudo instalar Flask. Ejecuta: pip3 install flask")
        sys.exit(1)

_ensure_flask()
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

state = dict(name=None, email=None, passphrase=None,
             key_id=None, fingerprint=None, coc_text=None, signed_coc=None)

setup_progress = dict(running=False, step="", detail="", done=False, ok=False, error="")

COC_URL       = "https://launchpad.net/codeofconduct/2.0/+download"
KEYSERVER_URL = "https://keyserver.ubuntu.com/pks/add"
KEYSERVER_ALT = "https://keys.openpgp.org/pks/add"

def _set_progress(step, detail=""):
    setup_progress["step"]   = step
    setup_progress["detail"] = detail

def _install_gpg_linux():
    managers = [
        ["apt-get", "install", "-y", "gnupg"],
        ["dnf",     "install", "-y", "gnupg2"],
        ["pacman",  "-S", "--noconfirm", "gnupg"],
        ["zypper",  "install", "-y", "gpg2"],
    ]
    for cmd in managers:
        if shutil.which(cmd[0]):
            _set_progress("Instalando GPG con {}...".format(cmd[0]))
            try:
                subprocess.run(["sudo"] + cmd, check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return shutil.which("gpg") is not None
            except Exception:
                continue
    return False

def _install_gpg_mac():
    if not shutil.which("brew"):
        _set_progress("Instalando Homebrew...", "Puede tardar varios minutos.")
        try:
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True, check=True)
        except Exception:
            return False
    _set_progress("Instalando GPG via Homebrew...", "Por favor espera.")
    try:
        subprocess.run(["brew", "install", "gnupg"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return shutil.which("gpg") is not None
    except Exception:
        return False

def _find_gpg_windows():
    """Busca gpg.exe en rutas conocidas de Gpg4win y actualiza el PATH."""
    known = [
        r"C:\Program Files (x86)\GnuPG\bin",
        r"C:\Program Files\GnuPG\bin",
        r"C:\Program Files\Gpg4win\bin",
        r"C:\Program Files (x86)\Gpg4win\bin",
    ]
    for p in known:
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "gpg.exe")):
            os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
            return True
    return False

def _install_gpg_windows():
    # Primero: buscar GPG ya instalado pero fuera del PATH del proceso
    if _find_gpg_windows() and shutil.which("gpg"):
        return True
    # Segundo: intentar instalar con gestores de paquetes
    # winget devuelve códigos especiales cuando el paquete ya está instalado
    WINGET_SUCCESS = {0, -1978335189, -1978335212, 3010}
    for mgr, cmd in [
        ("winget", ["winget", "install", "--id", "GnuPG.Gpg4win", "-e", "--silent"]),
        ("choco",  ["choco", "install", "gpg4win", "-y"]),
        ("scoop",  ["scoop", "install", "gpg"]),
    ]:
        if shutil.which(mgr):
            _set_progress("Instalando Gpg4win con {}...".format(mgr))
            try:
                result = subprocess.run(cmd,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                ok_codes = WINGET_SUCCESS if mgr == "winget" else {0}
                if result.returncode in ok_codes:
                    _find_gpg_windows()
                    return shutil.which("gpg") is not None
            except Exception:
                continue
    return False

def _ensure_gpg_async():
    setup_progress.update(running=True, done=False, ok=False, error="")
    _set_progress("Verificando si GPG esta instalado...",
                  "Comprobando herramientas disponibles.")
    time.sleep(0.3)
    if shutil.which("gpg"):
        _set_progress("GPG ya esta instalado.", "Todo listo!")
        time.sleep(0.6)
        setup_progress.update(done=True, ok=True, running=False)
        return
    # Windows: GPG puede estar instalado pero no en el PATH del proceso actual
    if IS_WINDOWS and _find_gpg_windows() and shutil.which("gpg"):
        _set_progress("GPG encontrado en el sistema.", "Todo listo!")
        time.sleep(0.6)
        setup_progress.update(done=True, ok=True, running=False)
        return
    _set_progress("GPG no encontrado. Instalando automaticamente...",
                  "Solo ocurre la primera vez.")
    time.sleep(0.5)
    if IS_LINUX:     ok = _install_gpg_linux()
    elif IS_MAC:     ok = _install_gpg_mac()
    elif IS_WINDOWS: ok = _install_gpg_windows()
    else:            ok = False
    if ok:
        _set_progress("GPG instalado correctamente.", "Todo listo!")
        time.sleep(0.5)
        setup_progress.update(done=True, ok=True, running=False)
    else:
        hints = {
            "Linux":   "sudo apt-get install gnupg",
            "Darwin":  "brew install gnupg",
            "Windows": "https://www.gpg4win.org/",
        }
        hint = hints.get(SYS, "https://gnupg.org/")
        setup_progress.update(done=True, ok=False, running=False,
            error="No se pudo instalar GPG.<br><b>Manual:</b> " + hint)

def run_gpg(args, input_data=None, timeout=90):
    cmd = ["gpg", "--no-tty", "--batch"] + args
    try:
        r = subprocess.run(cmd, input=input_data, capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Tiempo de espera agotado"
    except Exception as e:
        return 1, "", str(e)

def get_key_info(email):
    code, out, _ = run_gpg(["--list-keys", "--keyid-format", "LONG",
                             "--with-colons", email])
    if code != 0:
        return None, None
    key_id = fingerprint = None
    for line in out.splitlines():
        parts = line.split(":")
        if parts[0] == "pub" and len(parts) > 4:
            key_id = parts[4][-16:]
        if parts[0] == "fpr" and len(parts) > 9:
            fingerprint = parts[9]
    if fingerprint and not key_id:
        key_id = fingerprint[-16:]
    return key_id, fingerprint

def format_fingerprint(fp):
    if not fp: return ""
    clean = fp.upper().replace(" ", "")
    return " ".join(clean[i:i+4] for i in range(0, len(clean), 4))

@app.route("/")
def index():
    return HTML

@app.route("/api/start-setup", methods=["POST"])
def api_start_setup():
    if not setup_progress["running"]:
        threading.Thread(target=_ensure_gpg_async, daemon=True).start()
    return jsonify({"ok": True})

@app.route("/api/setup-status")
def api_setup_status():
    return jsonify({k: setup_progress[k] for k in
                    ["running","step","detail","done","ok","error"]})

@app.route("/api/generate-key", methods=["POST"])
def api_generate_key():
    data = request.get_json()
    name       = data.get("name", "").strip()
    email      = data.get("email", "").strip()
    passphrase = data.get("pass", "").strip()
    if not all([name, email, passphrase]):
        return jsonify({"ok": False, "error": "Faltan datos obligatorios"})
    existing_id, existing_fp = get_key_info(email)
    if existing_id:
        state.update(name=name, email=email, passphrase=passphrase,
                     key_id=existing_id, fingerprint=existing_fp)
        return jsonify({"ok": True, "key_id": existing_id, "existing": True})
    batch = (
        "%echo Generando llave\n"
        "Key-Type: RSA\nKey-Length: 4096\n"
        "Subkey-Type: RSA\nSubkey-Length: 4096\n"
        "Name-Real: {}\nName-Email: {}\n"
        "Expire-Date: 0\nPassphrase: {}\n%commit\n%echo done\n"
    ).format(name, email, passphrase)
    code, out, err = run_gpg(["--gen-key"], input_data=batch, timeout=300)
    if code != 0 and "done" not in (err + out):
        batch2 = (
            "Key-Type: RSA\nKey-Length: 4096\n"
            "Name-Real: {}\nName-Email: {}\n"
            "Expire-Date: 0\nPassphrase: {}\n%commit\n"
        ).format(name, email, passphrase)
        code, out, err = run_gpg(["--gen-key"], input_data=batch2, timeout=300)
    key_id, fingerprint = get_key_info(email)
    if not key_id:
        _, out2, _ = run_gpg(["--list-keys", "--keyid-format", "LONG", "--with-colons"])
        for line in out2.splitlines():
            parts = line.split(":")
            if parts[0] == "pub" and len(parts) > 4: key_id = parts[4][-16:]
            if parts[0] == "fpr" and len(parts) > 9:
                fingerprint = parts[9]; break
    if not key_id:
        return jsonify({"ok": False,
                        "error": "No se pudo verificar la llave. " + err[:300]})
    state.update(name=name, email=email, passphrase=passphrase,
                 key_id=key_id, fingerprint=fingerprint)
    return jsonify({"ok": True, "key_id": key_id})

@app.route("/api/publish-key", methods=["POST"])
def api_publish_key():
    key_id = state.get("key_id")
    if not key_id:
        return jsonify({"ok": False, "error": "No hay llave generada."})
    code, armored_key, err = run_gpg(["--armor", "--export", key_id])
    if code != 0 or not armored_key.strip():
        return jsonify({"ok": False, "error": "No se pudo exportar la llave: " + err[:200]})
    last_error = ""
    for ks_url in [KEYSERVER_URL, KEYSERVER_ALT]:
        try:
            payload = urllib.parse.urlencode({"keytext": armored_key}).encode("utf-8")
            req = urllib.request.Request(
                ks_url,
                data=payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Ubuntu-CoC-Wizard/3.2"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    return jsonify({"ok": True})
        except Exception as e:
            last_error = str(e)
            continue
    return jsonify({"ok": False, "error": "No se pudo publicar la llave: " + last_error[:200]})

@app.route("/api/fingerprint")
def api_fingerprint():
    fp = state.get("fingerprint")
    if not fp:
        return jsonify({"ok": False, "error": "No hay huella disponible"})
    return jsonify({"ok": True, "fingerprint": format_fingerprint(fp), "raw": fp})

@app.route("/api/decrypt-email", methods=["POST"])
def api_decrypt_email():
    data = request.get_json()
    content    = data.get("content", "").strip()
    passphrase = data.get("passphrase") or state.get("passphrase", "")
    if not content:
        return jsonify({"ok": False, "error": "Pega el contenido del correo cifrado"})
    code, out, err = run_gpg(
        ["--pinentry-mode", "loopback", "--passphrase", passphrase, "--decrypt"],
        input_data=content, timeout=30)
    if code != 0:
        code, out, err = run_gpg(["--decrypt"], input_data=content, timeout=30)
    decrypted = out or err
    urls = re.findall(r'https?://launchpad\.net[^\s\'"<>]+', decrypted)
    confirm_urls = [u for u in urls if "confirm" in u or "token" in u]
    url = confirm_urls[0] if confirm_urls else (urls[0] if urls else None)
    if url:
        return jsonify({"ok": True, "confirm_url": url, "decrypted": decrypted[:600]})
    if code == 0 and out:
        return jsonify({"ok": True, "confirm_url": "#", "decrypted": out,
                        "note": "Busca el enlace de confirmacion en el texto descifrado."})
    return jsonify({"ok": False,
                    "error": "No se pudo descifrar. Pega el correo completo con BEGIN/END PGP MESSAGE. (" + err[:200] + ")"})

@app.route("/api/sign-coc", methods=["POST"])
def api_sign_coc():
    data = request.get_json()
    passphrase = data.get("passphrase") or state.get("passphrase", "")
    key_id     = state.get("key_id")
    if not key_id:
        return jsonify({"ok": False, "error": "No hay llave GPG disponible"})
    coc_path = Path(tempfile.gettempdir()) / "UbuntuCodeofConduct-2.0.txt"
    try:
        req = urllib.request.Request(COC_URL, headers={"User-Agent": "Ubuntu-CoC-Wizard/3.2"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            coc_path.write_bytes(resp.read())
    except Exception as e:
        return jsonify({"ok": False, "error": "No se pudo descargar el CoC: " + str(e)})
    signed_path = str(coc_path) + ".asc"
    if os.path.exists(signed_path):
        os.remove(signed_path)
    code, _, err = run_gpg(
        ["--pinentry-mode", "loopback", "--passphrase", passphrase,
         "--default-key", key_id, "--clearsign", "--output", signed_path, str(coc_path)],
        timeout=30)
    if code != 0 or not os.path.exists(signed_path):
        return jsonify({"ok": False, "error": "No se pudo firmar el CoC: " + err[:200]})
    state["signed_coc"]  = Path(signed_path).read_text()
    state["passphrase"]  = None
    return jsonify({"ok": True})

@app.route("/api/signed-coc")
def api_signed_coc():
    signed = state.get("signed_coc")
    if not signed:
        return jsonify({"ok": False, "error": "No hay CoC firmado"})
    return jsonify({"ok": True, "signed": signed})

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Firma el Codigo de Conducta de Ubuntu</title>
<style>
:root{--orange:#E95420;--carbon:#262626;--anthracite:#333;--border:#d9d9d9;--text:#111;--text-muted:#666;--text-light:#ccc;--green:#0E8420;--bg-page:#262626;--bg-card:#fff;--bg-dark:#333;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:Ubuntu,'Segoe UI',sans-serif;background:var(--bg-page);min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:0;}
.site-topbar{width:100%;background:#000;border-bottom:1px solid #111;min-height:2.5rem;display:flex;justify-content:center;}
.site-topbar-inner{max-width:72rem;width:100%;padding:0 1rem;display:flex;justify-content:space-between;align-items:center;height:2.5rem;}
.site-topbar a{color:#666;font-size:0.85rem;text-decoration:none;font-weight:300;}
.site-topbar a:hover{color:#999;}
.site-navbar{width:100%;background:var(--carbon);border-bottom:1px solid #333;min-height:56px;display:flex;justify-content:center;}
.site-navbar-inner{max-width:72rem;width:100%;padding:0 1rem;display:flex;align-items:stretch;}
.site-navbar-brand{display:flex;align-items:center;gap:1rem;padding:0.8rem 1.5rem;background-color:var(--orange);color:#fff;text-decoration:none;font-weight:400;font-size:1.1rem;letter-spacing:0.5px;white-space:nowrap;}
.site-navbar-brand:hover{background-color:#C8421A;}
.site-actionbar{width:100%;background:var(--bg-dark);border-bottom:1px solid #444;min-height:48px;display:flex;justify-content:center;}
.site-actionbar-inner{max-width:72rem;width:100%;padding:0 1rem;display:flex;align-items:center;gap:2rem;}
.site-actionbar a{color:var(--text-light);font-size:0.9rem;text-decoration:none;padding:0.7rem 0;}
.site-actionbar a:hover{color:#fff;}
#progress-bar-wrap{width:100%;max-width:72rem;padding:24px 1rem 0;margin-bottom:12px;}
.progress-steps{display:flex;align-items:flex-start;justify-content:space-between;position:relative;padding:0 0 4px 0;}
.progress-steps::before{content:'';position:absolute;top:17px;left:18px;right:18px;height:3px;background:rgba(255,255,255,0.12);z-index:0;border-radius:2px;}
.progress-line-fill{position:absolute;top:17px;left:18px;height:3px;background:linear-gradient(90deg,var(--orange),#ff8c42);z-index:1;border-radius:2px;transition:width 0.6s cubic-bezier(.4,0,.2,1);width:0%;}
.ps{flex:1;display:flex;flex-direction:column;align-items:center;position:relative;z-index:2;}
.ps-bubble{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.08);border:2px solid rgba(255,255,255,0.18);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:rgba(255,255,255,0.3);transition:all 0.4s cubic-bezier(.4,0,.2,1);position:relative;}
.ps-label{font-size:9px;font-weight:600;color:rgba(255,255,255,0.28);margin-top:5px;text-align:center;line-height:1.2;transition:color 0.3s;}
.ps.done .ps-bubble{background:#2E7D32;border-color:#4CAF50;color:#fff;animation:pop-in 0.3s cubic-bezier(.4,0,.2,1) both;}
.ps.active .ps-bubble::after{content:'';position:absolute;width:36px;height:36px;border-radius:50%;border:3px solid var(--orange);animation:ripple 1.4s ease-out infinite;pointer-events:none;}
.ps.done .ps-label{color:#81C784;}
.ps.active .ps-bubble{background:var(--orange);border-color:var(--orange);color:white;transform:scale(1.18);box-shadow:0 0 0 5px rgba(233,84,32,0.25);animation:step-in 0.35s cubic-bezier(.4,0,.2,1) both;}
.ps.active .ps-label{color:white;font-weight:700;}
@keyframes step-in{from{transform:scale(0.5);opacity:0;}to{transform:scale(1.18);opacity:1;}}
@keyframes ripple{0%{transform:scale(1);opacity:0.7;}100%{transform:scale(2.2);opacity:0;}}
@keyframes pop-in{0%{transform:scale(0.7);opacity:0.3;}60%{transform:scale(1.15);}100%{transform:scale(1);opacity:1;}}
.progress-box{background:var(--bg-dark);color:white;border-radius:4px;padding:20px;text-align:center;margin:6px 0 16px;border:1px solid rgba(255,255,255,0.1);}
.progress-box .step-text{font-size:16px;font-weight:400;margin-bottom:6px;}
.progress-box .detail-text{font-size:13px;color:var(--text-light);margin-bottom:15px;min-height:18px;}
.spinner{display:inline-block;width:32px;height:32px;border:4px solid rgba(255,255,255,.2);border-top-color:var(--orange);border-radius:50%;animation:spin .8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}
header{width:100%;max-width:72rem;text-align:left;padding:24px 1rem 16px;color:white;}
header h1{font-size:1.8rem;font-weight:100;color:white;line-height:1.3;}
header p{color:var(--text-light);margin-top:6px;font-size:0.9rem;}
.card{background:var(--bg-card);border-radius:0.125rem;padding:1.5rem;width:100%;max-width:72rem;margin:0 auto 16px;box-shadow:0 1px 1px 0 rgba(0,0,0,0.15),0 2px 2px -1px rgba(0,0,0,0.15),0 0 3px 0 rgba(0,0,0,0.2);border:1px solid var(--border);}
.step-badge{display:inline-flex;align-items:center;background:var(--orange);color:white;border-radius:2px;padding:3px 13px;font-size:11px;font-weight:700;margin-bottom:11px;text-transform:uppercase;}
h2{color:var(--text);font-size:1.4rem;margin-bottom:9px;font-weight:100;}
.description{color:#333;line-height:1.65;margin-bottom:16px;font-size:14px;}
.description strong{color:var(--text);}
label{display:block;font-weight:400;color:var(--text);margin-bottom:5px;font-size:13px;}
input[type=text],input[type=email],input[type=password],textarea{width:100%;padding:11px 13px;border:1px solid var(--border);border-radius:0.125rem;font-size:14px;font-family:inherit;transition:border-color .2s;margin-bottom:13px;color:var(--text);background:#fff;}
input:focus,textarea:focus{outline:none;border-color:var(--orange);background:white;}
textarea{resize:vertical;min-height:130px;font-family:monospace;font-size:13px;}
.btn{display:inline-flex;align-items:center;gap:7px;padding:0.7rem 1.5rem;border:none;border-radius:0.125rem;font-size:14px;font-weight:400;cursor:pointer;transition:all .2s;font-family:inherit;text-decoration:none;}
.btn-primary{background:var(--orange);color:white;}
.btn-primary:hover:not(:disabled){background:#C8421A;transform:translateY(-1px);}
.btn-primary:disabled{background:#999;cursor:not-allowed;}
.btn-secondary{background:transparent;color:var(--orange);border:1px solid var(--orange);}
.btn-secondary:hover{background:#FFF0EB;}
.btn-success{background:var(--green);color:white;}
.alert{padding:12px 15px;border-radius:0.125rem;margin-bottom:13px;font-size:13px;line-height:1.6;}
.alert-info{background:#E8F4FD;color:#1565C0;border-left:4px solid #1565C0;}
.alert-success{background:#E8F5E9;color:#2E7D32;border-left:4px solid #2E7D32;}
.alert-warning{background:#FFF8E1;color:#F57F17;border-left:4px solid #F57F17;}
.alert-error{background:#FFEBEE;color:#C62828;border-left:4px solid #C62828;}
.fingerprint-box{background:#f7f7f7;border:1px solid var(--border);border-radius:0.125rem;padding:13px;font-family:monospace;font-size:14px;letter-spacing:2px;color:var(--text);text-align:center;margin:10px 0 16px;word-break:break-all;}
.signed-output{background:#1a1a1a;color:#ccc;border-radius:0.125rem;padding:13px;font-family:monospace;font-size:11px;max-height:190px;overflow-y:auto;white-space:pre-wrap;word-break:break-all;margin-bottom:13px;}
.step-list{counter-reset:sc;list-style:none;padding:0;}
.step-list li{counter-increment:sc;display:flex;align-items:flex-start;gap:10px;padding:9px 0;border-bottom:1px solid var(--border);font-size:13px;color:#333;line-height:1.5;}
.step-list li:last-child{border-bottom:none;}
.step-list li::before{content:counter(sc);min-width:24px;height:24px;background:var(--orange);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;}
.hidden{display:none!important;}
.section{margin-bottom:10px;}
code{background:#f7f7f7;padding:2px 5px;border-radius:0.125rem;font-family:monospace;font-size:12px;color:var(--text);}
.row-btns{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.pass-wrap{position:relative;}
.pass-wrap input{padding-right:42px;margin-bottom:3px;}
.pass-wrap button{position:absolute;right:9px;top:11px;background:none;border:none;cursor:pointer;font-size:17px;}
.pass-hint{font-size:12px;color:#888;margin-bottom:13px;}
.highlight-box{background:#f7f7f7;border-left:4px solid var(--orange);border-radius:0 0.125rem 0.125rem 0;padding:13px 17px;margin-bottom:14px;font-size:13px;color:#333;line-height:1.6;}
.highlight-box strong{color:var(--orange);}
.login-notice{background:var(--bg-dark);color:white;border-radius:0.125rem;padding:13px 17px;margin-bottom:14px;font-size:13px;line-height:1.6;border-left:4px solid var(--orange);}
.login-notice a{color:var(--orange);font-weight:400;}
.wait-badge{display:inline-block;background:#FFF3E0;border:1px solid var(--orange);color:var(--orange);border-radius:2px;padding:2px 8px;font-size:11px;font-weight:700;vertical-align:middle;}
footer.site-footer{width:100%;background:#000;border-top:1px solid #111;padding:1.5rem 0;text-align:center;color:#666;font-size:0.8rem;}
footer.site-footer a{color:#888;text-decoration:none;margin:0 1rem;}
</style>
</head>
<body>

<!-- BARRA GLOBAL SUPERIOR (Negro Puro - igual al sitio Hugo) -->
<div class="site-topbar">
  <div class="site-topbar-inner">
    <a href="https://ubuntu-ve.org">Canonical Ubuntu</a>
    <div style="display:flex;gap:1.5rem;">
      <a href="https://ubuntu.com">All Canonical</a>
      <a href="https://ubuntu-ve.org/admin/">Sign in</a>
    </div>
  </div>
</div>

<!-- NAVEGACION (Gris Carbono - igual al sitio Hugo) -->
<div class="site-navbar">
  <div class="site-navbar-inner">
    <a class="site-navbar-brand" href="https://ubuntu-ve.org">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="#fff"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 2.2c5.412 0 9.8 4.388 9.8 9.8s-4.388 9.8-9.8 9.8-9.8-4.388-9.8-9.8 4.388-9.8 9.8-9.8zm0 2.4c-4.087 0-7.4 3.313-7.4 7.4s3.313 7.4 7.4 7.4 7.4-3.313 7.4-7.4-3.313-7.4-7.4-7.4z"/></svg>
      Ubuntu Venezuela
    </a>
  </div>
</div>

<!-- ACTION BAR (Gris Antracita - igual al sitio Hugo) -->
<div class="site-actionbar">
  <div class="site-actionbar-inner">
    <a href="https://ubuntu-ve.org/codigo-de-conducta/">Codigo de Conducta</a>
    <a href="https://ubuntu-ve.org/about/">La comunidad</a>
    <a href="https://ubuntu-ve.org/miembros/">Miembros</a>
  </div>
</div>

<div id="progress-bar-wrap">
  <div class="progress-steps">
    <div class="progress-line-fill" id="progress-line-fill"></div>
    <div class="ps active" id="ps0"><div class="ps-bubble">&#127968;</div><span class="ps-label">Inicio</span></div>
    <div class="ps" id="ps1"><div class="ps-bubble">1</div><span class="ps-label">Launchpad</span></div>
    <div class="ps" id="ps2"><div class="ps-bubble">2</div><span class="ps-label">Mi llave</span></div>
    <div class="ps" id="ps3"><div class="ps-bubble">3</div><span class="ps-label">Publicar</span></div>
    <div class="ps" id="ps4"><div class="ps-bubble">4</div><span class="ps-label">Registrar</span></div>
    <div class="ps" id="ps5"><div class="ps-bubble">5</div><span class="ps-label">Correo</span></div>
    <div class="ps" id="ps6"><div class="ps-bubble">6</div><span class="ps-label">Firmar</span></div>
    <div class="ps" id="ps7"><div class="ps-bubble">&#10003;</div><span class="ps-label">Listo!</span></div>
  </div>
</div>

<header>
  <h1>Codigo de Conducta de Ubuntu</h1>
  <p>Asistente de firma paso a paso &mdash; v3.2</p>
</header>

<div id="screen-welcome" class="card">
  <h2>Bienvenido/a!</h2>
  <p class="description">Firmar el Codigo de Conducta de Ubuntu es tu manera de comprometerte con los valores de nuestra comunidad: <strong>respeto, colaboracion y apertura</strong>.<br><br>Este asistente te guiara en cada paso. <strong>No necesitas conocimientos tecnicos</strong>.</p>
  <div id="setup-progress-box" class="progress-box hidden">
    <div class="step-text" id="prog-step">Estamos preparando todo, por favor espera...</div>
    <div class="detail-text" id="prog-detail">Verificando las herramientas necesarias.</div>
    <div class="spinner" id="prog-spinner"></div>
  </div>
  <div id="setup-error-box" class="alert alert-error hidden"></div>
  <button class="btn btn-primary" id="btn-start" onclick="startSetup()">Comenzar</button>
</div>

<div id="screen-step1" class="card hidden">
  <div class="step-badge">Paso 1 de 6</div>
  <h2>Crea tu cuenta en Launchpad</h2>
  <p class="description"><strong>Launchpad</strong> es la plataforma oficial de Ubuntu donde quedara registrada tu firma. Si ya tienes cuenta, continua al siguiente paso.</p>
  <div class="alert alert-info">Nota: Usa el <strong>mismo correo electronico</strong> en Launchpad y en este asistente.</div>
  <div style="background:#FFEBEE;color:#C62828;border-left:4px solid #C62828;padding:12px 15px;border-radius:8px;margin-bottom:13px;font-size:13px;line-height:1.6;">
    <strong>(!) &iquest;No tienes cuenta en Launchpad?</strong> Deber&aacute;s <a href="https://login.launchpad.net/+login" target="_blank" style="color:#C62828;font-weight:700;text-decoration:underline;">crear una cuenta</a> antes de continuar. Una vez registrado, Launchpad enviar&aacute; un correo para <strong>verificar tu cuenta</strong> &mdash; haz clic en el enlace de verificaci&oacute;n antes de seguir con este asistente.
  </div>
  <div class="alert alert-warning" id="step1-confirm-box">
    <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:14px;">
      <input type="checkbox" id="chk-launchpad-confirmed" onchange="toggleStep1Next()" style="width:18px;height:18px;accent-color:#E95420;">
      <span>[X] Confirmo que tengo cuenta en Launchpad <strong>y</strong> que ya verifiqu&eacute; mi correo electr&oacute;nico.</span>
    </label>
  </div>
  <div class="row-btns">
    <a href="https://login.launchpad.net/+login" target="_blank" class="btn btn-secondary">Crear cuenta en Launchpad</a>
    <button class="btn btn-primary" id="btn-step1-next" onclick="goTo('screen-step2',2)" disabled style="opacity:0.5;cursor:not-allowed;">Ya tengo cuenta &rarr;</button>
  </div>
</div>

<div id="screen-step2" class="card hidden">
  <div class="step-badge">Paso 2 de 6</div>
  <h2>Crea tu llave digital</h2>
  <p class="description">Tu <strong>llave GPG</strong> es como un sello digital unico. Nadie mas puede usarla &mdash; solo tu, con tu contrasena.</p>
  <div class="section">
    <label for="inp-name">Tu nombre completo</label>
    <input type="text" id="inp-name" placeholder="Ej: Ana Garcia Lopez" autocomplete="name">
  </div>
  <div class="section">
    <label for="inp-email">Correo electronico (el mismo de Launchpad)</label>
    <input type="email" id="inp-email" placeholder="Ej: ana@ejemplo.com" autocomplete="email">
  </div>
  <div class="section">
    <label for="inp-pass">Contrasena para proteger tu llave</label>
    <div class="pass-wrap">
      <input type="password" id="inp-pass" placeholder="Elige una contrasena segura">
      <button type="button" onclick="togglePass('inp-pass',this)">Ver</button>
    </div>
    <p class="pass-hint">&#9888;&#65039; Guarda esta contrasena, la necesitaras en los pasos siguientes.</p>
  </div>
  <div id="key-progress" class="progress-box hidden">
    <div class="step-text">&#128272; Generando tu llave RSA-4096...</div>
    <div class="detail-text">Puede tardar hasta 30 segundos.</div>
    <div class="spinner"></div>
  </div>
  <div id="key-result" class="hidden"></div>
  <div class="row-btns">
    <button class="btn btn-secondary" onclick="goTo('screen-step1',1)">&larr; Atras</button>
    <button class="btn btn-primary" id="btn-genkey" onclick="generateKey()">Crear mi llave digital</button>
  </div>
</div>

<div id="screen-step3" class="card hidden">
  <div class="step-badge">Paso 3 de 6</div>
  <h2>Publica tu llave en el servidor de Ubuntu</h2>
  <p class="description">Necesitamos publicar tu llave en <code>keyserver.ubuntu.com</code> para que Launchpad pueda encontrarla.</p>
  <div class="highlight-box">
    &#128273; <strong>&iquest;Por qu&eacute; debo subir mi llave p&uacute;blica?</strong><br>
    Cuando Launchpad recibe tu huella digital, necesita <strong>descargar tu llave p&uacute;blica</strong> desde un servidor de confianza para verificar tu identidad. <code>keyserver.ubuntu.com</code> act&uacute;a como directorio p&uacute;blico de llaves GPG &mdash; sin este paso, Launchpad <strong>no podr&aacute; importar tu llave</strong>.
  </div>
  <div class="alert alert-warning">&#9203; <strong>Importante:</strong> Despues de publicar, espera <strong>10 minutos</strong> antes del siguiente paso para que el servidor indexe tu llave.</div>
  <div id="pub-progress" class="progress-box hidden">
    <div class="step-text">&#128225; Publicando tu llave via HTTPS...</div>
    <div class="detail-text">Conectando con keyserver.ubuntu.com.</div>
    <div class="spinner"></div>
  </div>
  <div id="pub-result" class="hidden"></div>
  <div class="row-btns">
    <button class="btn btn-secondary" onclick="goTo('screen-step2',2)">&larr; Atras</button>
    <button class="btn btn-primary" id="btn-publish" onclick="publishKey()">Publicar mi llave</button>
  </div>
</div>

<div id="screen-step4" class="card hidden">
  <div class="step-badge">Paso 4 de 6</div>
  <h2>Registra tu llave en Launchpad</h2>
  <div class="login-notice">
    &#128272; <strong>Antes de continuar:</strong> asegurate de haber iniciado sesion en Launchpad.
    Si no lo has hecho, <a href="https://launchpad.net/+login" target="_blank">haz clic aqui para iniciar sesion</a> y luego vuelve a este paso.
  </div>
  <div class="alert alert-warning">
    &#9203; <span class="wait-badge">ESPERA MIN</span>&nbsp;
    Si acabas de publicar tu llave, <strong>espera algunos minutos</strong> antes de continuar.
    Si lo haces antes, Launchpad mostrara el error <em>could not import your OpenPGP key</em>.
    Puedes tomarte unos minutos y volver.
  </div>
  <p class="description">Cuando hayas esperado, sigue estos pasos exactamente:</p>
  <ol class="step-list">
    <li>Copia la <strong>huella digital</strong> de abajo con el boton Copiar huella.</li>
    <li>Haz clic en el boton naranja <strong>Ir a la seccion GPG de Launchpad</strong>. Te llevara directamente a <code>launchpad.net/people/me/+editpgpkeys</code>.</li>
    <li>En esa pagina busca la seccion <strong>Import an OpenPGP key</strong>. Pega la huella en el campo <strong>Fingerprint</strong> en negrilla y presiona el boton <strong>Import Key</strong>.</li>
    <li>Launchpad enviara un <strong>correo cifrado</strong> a tu email. Abrelo y vuelve aqui.</li>
  </ol>
  <div id="fp-box" class="fingerprint-box">Cargando huella digital...</div>
  <button class="btn btn-secondary" id="btn-copy-fp" onclick="copyFingerprint()" style="margin-bottom:16px">Copiar huella</button>
  <div class="highlight-box">
    &#128073; El boton naranja te lleva <strong>directamente a la seccion correcta</strong> de Launchpad. No navegues a otra pagina.
  </div>
  <div class="row-btns">
    <button class="btn btn-secondary" onclick="goTo('screen-step3',3)">&larr; Atras</button>
    <a href="https://launchpad.net/people/+me/+editpgpkeys" target="_blank" class="btn btn-primary">&#128273; Ir a la seccion GPG de Launchpad &rarr;</a>
    <button class="btn btn-primary" onclick="goTo('screen-step5',5)" style="background:#555;font-size:13px">Ya lo hice &rarr;</button>
  </div>
</div>

<div id="screen-step5" class="card hidden">
  <div class="step-badge">Paso 5 de 6</div>
  <h2>Descifra el correo de Launchpad</h2>
  <p class="description">Launchpad te envio un correo <strong>cifrado</strong>. Abrelo, copia todo su contenido desde <code>-----BEGIN PGP MESSAGE-----</code> hasta <code>-----END PGP MESSAGE-----</code> y pegalo abajo.</p>
  <div class="alert alert-warning">&#9203; Espera 2-3 minutos antes de buscar el correo. Revisa tambien la carpeta de <strong>spam</strong>.</div>
  <label for="inp-email-content">Contenido del correo cifrado</label>
  <textarea id="inp-email-content" placeholder="-----BEGIN PGP MESSAGE-----&#10;...&#10;-----END PGP MESSAGE-----"></textarea>
  <div class="section">
    <label for="inp-pass2">Contrasena de tu llave GPG</label>
    <div class="pass-wrap">
      <input type="password" id="inp-pass2" placeholder="La contrasena del paso 2">
      <button type="button" onclick="togglePass('inp-pass2',this)">Ver</button>
    </div>
  </div>
  <div id="dec-progress" class="progress-box hidden">
    <div class="step-text">&#128275; Descifrando el correo...</div>
    <div class="detail-text">Un momento.</div>
    <div class="spinner"></div>
  </div>
  <div id="dec-result" class="hidden"></div>
  <div class="row-btns">
    <button class="btn btn-secondary" onclick="goTo('screen-step4',4)">&larr; Atras</button>
    <button class="btn btn-primary" id="btn-decrypt" onclick="decryptEmail()">Descifrar correo</button>
  </div>
</div>

<div id="screen-step6" class="card hidden">
  <div class="step-badge">Paso 6 de 6</div>
  <h2>Firma el Codigo de Conducta</h2>
  <p class="description">Ultimo paso! Descargaremos el Codigo de Conducta y lo firmaremos digitalmente.</p>
  <div class="alert alert-info">&#128161; Asegurate de haber confirmado el enlace que llego a tu correo desde Launchpad antes de continuar.</div>
  <div class="section">
    <label for="inp-pass3">Contrasena de tu llave GPG</label>
    <div class="pass-wrap">
      <input type="password" id="inp-pass3" placeholder="La contrasena de tu llave">
      <button type="button" onclick="togglePass('inp-pass3',this)">Ver</button>
    </div>
  </div>
  <div id="sign-progress" class="progress-box hidden">
    <div class="step-text">&#9998; Firmando el Codigo de Conducta...</div>
    <div class="detail-text">Descargando y firmando. Un momento.</div>
    <div class="spinner"></div>
  </div>
  <div id="sign-result" class="hidden"></div>
  <div id="signed-output-wrap" class="hidden">
    <label>Texto firmado &mdash; copialo y pegalo en Launchpad:</label>
    <div class="signed-output" id="signed-output"></div>
    <div class="row-btns" style="margin-bottom:13px">
      <button class="btn btn-secondary" onclick="copySignedCoC()">Copiar texto firmado</button>
      <a href="https://launchpad.net/codeofconduct/2.0/+sign" target="_blank" class="btn btn-primary">&#127760; Pegar en Launchpad &rarr;</a>
      <button class="btn btn-success" onclick="goTo('screen-done',7)">&#10003; He pegado el texto, Finalizar!</button>
    </div>
  </div>
  <div class="row-btns" id="sign-btns">
    <button class="btn btn-secondary" onclick="goTo('screen-step5',5)">&larr; Atras</button>
    <button class="btn btn-primary" id="btn-sign" onclick="signCoC()">Firmar el Codigo de Conducta</button>
  </div>
</div>

<div id="screen-done" class="card hidden" style="text-align:center">
  <div style="font-size:58px;margin-bottom:12px;display:none"></div>
  <h2 style="color:var(--green)">Felicitaciones!</h2>
  <p class="description" style="text-align:center;margin-top:10px">Eres oficialmente parte de la comunidad Ubuntu. Tu compromiso con los valores de <strong>respeto, colaboracion y apertura</strong> queda registrado para siempre.</p>
  <div class="alert alert-success" style="margin-top:16px">&#10003; Has firmado exitosamente el Codigo de Conducta de Ubuntu!</div>
</div>

<footer class="site-footer">
  Ubuntu Venezuela &mdash; Codigo de Conducta Wizard v3.2
  <br>
  <span style="font-size: 0.7rem; color: #444; font-style: italic;">
    Este script es un fork mejorado basado en el trabajo original de <a href="https://ubuntu.co" style="color: #666; text-decoration: underline;">Ubuntu Colombia</a>.
  </span>
  <br><br>
  <a href="https://ubuntu-ve.org">ubuntu-ve.org</a>
  <a href="https://ubuntu.com/legal">Información Legal</a>
  <a href="mailto:junta@ubuntu-ve.org">Contacto</a>
</footer>

<script>
function toggleStep1Next(){
  const chk=document.getElementById('chk-launchpad-confirmed');
  const btn=document.getElementById('btn-step1-next');
  if(chk.checked){btn.disabled=false;btn.style.opacity='1';btn.style.cursor='pointer';}
  else{btn.disabled=true;btn.style.opacity='0.5';btn.style.cursor='not-allowed';}
}
function updateProgressBar(idx){
  const total=7;
  for(let i=0;i<=total;i++){
    const el=document.getElementById("ps"+i);
    if(!el)continue;
    el.classList.remove("active","done");
    if(i<idx)el.classList.add("done");
    else if(i===idx)el.classList.add("active");
  }
  const fill=document.getElementById("progress-line-fill");
  if(fill){
    const pct=idx===0?0:Math.min((idx/total)*100,100);
    fill.style.width=pct+"%";
  }
}
function showScreen(id){
  document.querySelectorAll(".card").forEach(c=>c.classList.add("hidden"));
  document.getElementById(id).classList.remove("hidden");
  window.scrollTo({top:0,behavior:"smooth"});
}
function goTo(screenId,stepIdx){
  showScreen(screenId);
  updateProgressBar(stepIdx);
  if(screenId==="screen-step4")loadFingerprint();
}
function togglePass(id,btn){
  const inp=document.getElementById(id);
  const show=inp.type==="password";
  inp.type=show?"text":"password";
  btn.textContent=show?"Ocultar":"Ver";
}
function copyText(text){
  navigator.clipboard.writeText(text).catch(()=>{
    const ta=document.createElement("textarea");
    ta.value=text;document.body.appendChild(ta);
    ta.select();document.execCommand("copy");
    document.body.removeChild(ta);
  });
}
let pollInterval=null;
async function startSetup(){
  const btn=document.getElementById("btn-start");
  btn.disabled=true;btn.textContent="Preparando...";
  const box=document.getElementById("setup-progress-box");
  box.classList.remove("hidden");
  try{await fetch("/api/start-setup",{method:"POST"});}
  catch(e){showSetupError("No se pudo conectar. Recarga la pagina.");btn.disabled=false;btn.textContent="Comenzar";return;}
  pollInterval=setInterval(async()=>{
    try{
      const r=await fetch("/api/setup-status");const d=await r.json();
      if(d.step)document.getElementById("prog-step").textContent=d.step;
      if(d.detail)document.getElementById("prog-detail").textContent=d.detail;
      if(d.done){
        clearInterval(pollInterval);
        document.getElementById("prog-spinner").style.display="none";
        if(d.ok){
          document.getElementById("prog-step").textContent="Todo listo!";
          setTimeout(()=>goTo("screen-step1",1),800);
        } else {
          box.classList.add("hidden");
          showSetupError(d.error||"No se pudo instalar GPG.");
          btn.disabled=false;btn.textContent="Intentar de nuevo";
        }
      }
    }catch(e){}
  },800);
}
function showSetupError(msg){
  const eb=document.getElementById("setup-error-box");
  eb.innerHTML="&#10060; "+msg;eb.classList.remove("hidden");
}
async function generateKey(){
  const name=document.getElementById("inp-name").value.trim();
  const email=document.getElementById("inp-email").value.trim();
  const pass=document.getElementById("inp-pass").value.trim();
  if(!name||!email||!pass){alert("Por favor completa todos los campos.");return;}
  const btn=document.getElementById("btn-genkey");btn.disabled=true;btn.textContent="Generando...";
  show("key-progress");hide("key-result");
  try{
    const r=await fetch("/api/generate-key",{method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({name,email,pass})});
    const d=await r.json();hide("key-progress");
    if(d.ok){
      showResult("key-result",d.existing?"Llave existente encontrada. ID: <code>"+d.key_id+"</code>":"Llave creada! ID: <code>"+d.key_id+"</code>","success");
      setTimeout(()=>goTo("screen-step3",3),1500);
    } else {showResult("key-result","Error: "+d.error,"error");}
  }catch(e){hide("key-progress");showResult("key-result","Error: "+e.message,"error");}
  btn.disabled=false;btn.textContent="Crear mi llave digital";
}
async function publishKey(){
  const btn=document.getElementById("btn-publish");btn.disabled=true;btn.textContent="Publicando...";
  show("pub-progress");hide("pub-result");
  try{
    const r=await fetch("/api/publish-key",{method:"POST"});
    const d=await r.json();hide("pub-progress");
    if(d.ok){
      showResult("pub-result","Llave publicada exitosamente en keyserver.ubuntu.com!<br>&#9203; Espera <strong>10 minutos</strong> antes de continuar con el paso 4.","success");
      await loadFingerprint();
      setTimeout(()=>goTo("screen-step4",4),4000);
    } else {showResult("pub-result","Error: "+d.error,"error");}
  }catch(e){hide("pub-progress");showResult("pub-result","Error: "+e.message,"error");}
  btn.disabled=false;btn.textContent="Publicar mi llave";
}
let rawFingerprint="";
async function loadFingerprint(){
  try{
    const r=await fetch("/api/fingerprint");const d=await r.json();
    if(d.ok){document.getElementById("fp-box").textContent=d.fingerprint;rawFingerprint=d.raw;}
  }catch(e){}
}
function copyFingerprint(){
  copyText(rawFingerprint||document.getElementById("fp-box").textContent);
  document.getElementById("btn-copy-fp").textContent="Copiado!";
  setTimeout(()=>document.getElementById("btn-copy-fp").innerHTML="Copiar huella",2000);
}
async function decryptEmail(){
  const content=document.getElementById("inp-email-content").value.trim();
  const pass=document.getElementById("inp-pass2").value.trim();
  if(!content){alert("Pega el contenido del correo cifrado primero.");return;}
  const btn=document.getElementById("btn-decrypt");btn.disabled=true;btn.textContent="Descifrando...";
  show("dec-progress");hide("dec-result");
  try{
    const r=await fetch("/api/decrypt-email",{method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({content,passphrase:pass})});
    const d=await r.json();hide("dec-progress");
    if(d.ok){
      let html="Correo descifrado correctamente!";
      if(d.confirm_url&&d.confirm_url!="#")
        html+="<br><a href='"+d.confirm_url+"' target='_blank' style='color:#E95420;font-weight:700'>Haz clic aqui para confirmar en Launchpad</a>";
      else if(d.note) html+="<br>"+d.note;
      showResult("dec-result",html,"success");
      setTimeout(()=>goTo("screen-step6",6),3000);
    } else {showResult("dec-result","Error: "+d.error,"error");}
  }catch(e){hide("dec-progress");showResult("dec-result","Error: "+e.message,"error");}
  btn.disabled=false;btn.textContent="Descifrar correo";
}
async function signCoC(){
  const pass=document.getElementById("inp-pass3").value.trim();
  const btn=document.getElementById("btn-sign");btn.disabled=true;btn.textContent="Firmando...";
  show("sign-progress");hide("sign-result");hide("signed-output-wrap");
  try{
    const r=await fetch("/api/sign-coc",{method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({passphrase:pass})});
    const d=await r.json();hide("sign-progress");
    if(d.ok){
      showResult("sign-result","Codigo de Conducta firmado!","success");
      const r2=await fetch("/api/signed-coc");const d2=await r2.json();
      if(d2.ok){
        document.getElementById("signed-output").textContent=d2.signed;
        show("signed-output-wrap");hide("sign-btns");
      }
    } else {showResult("sign-result","Error: "+d.error,"error");}
  }catch(e){hide("sign-progress");showResult("sign-result","Error: "+e.message,"error");}
  btn.disabled=false;btn.textContent="Firmar el Codigo de Conducta";
}
function copySignedCoC(){
  copyText(document.getElementById("signed-output").textContent);
  alert("Texto copiado! Ahora pegalo en Launchpad.");
}
function show(id){document.getElementById(id).classList.remove("hidden");}
function hide(id){document.getElementById(id).classList.add("hidden");}
function showResult(id,html,type){
  const el=document.getElementById(id);
  el.className="alert alert-"+type;
  el.innerHTML=html;
  el.classList.remove("hidden");
}
</script>
</body>
</html>
"""

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("="*56)
    print("  Ubuntu Code of Conduct Wizard v3.2")
    print("  Abre tu navegador en http://127.0.0.1:5000")
    print("  Presiona Ctrl+C para detener el asistente.")
    print("="*56)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)