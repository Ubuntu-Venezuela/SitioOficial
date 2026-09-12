# Ripwire Setup — Replicar en Otro Equipo

## Qué es
Ripwire es un CLI + MCP server que da a los agentes de código mapas determinísticos del repo: qué leer primero, blast radius de un cambio, qué tests correr. Ahorra 5-300x tokens vs grep+read a ciegas.

## Requisitos
- WSL2 con Ubuntu (en Windows) o Linux nativo
- curl

## Instalación (5 min)

### 1. Instalar Ripwire en WSL/Linux
```bash
RIPWIRE_REPO=redhat-et/ripwire RIPWIRE_INSTALL_YES=1 bash -c "$(curl -fsSL https://raw.githubusercontent.com/redhat-et/ripwire/main/scripts/install.sh)"
```
El instalador deja el binario en `~/.local/bin/ripwire`.

**Importante (Windows/WSL):** asegurar que el PATH persista para shells NO interactivos (`bash -lc`), no solo interactivos. El `.bashrc` default de Ubuntu tiene un `return` temprano para shells no interactivos — la línea de PATH debe ir ANTES de ese return (top del archivo) y también en `.profile`:
```bash
sed -i '1i export PATH="$HOME/.local/bin:$PATH"' ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
```

### 2. Configurar MCP en opencode — SOLO global, nunca duplicar
Única fuente de verdad: `~/.config/opencode/opencode.jsonc`. **No** crear `opencode.json` en el proyecto con la misma entrada `mcp.ripwire` — la config de proyecto pisa la global y duplica servers MCP.

```jsonc
{
  "mcp": {
    "ripwire": {
      "type": "local",
      "enabled": true,
      "command": ["wsl", "bash", "-c", "exec \"$HOME/.local/bin/ripwire\" --mcp"]
    }
  }
}
```

**Por qué esta forma y no `export PATH=...; exec ripwire`:** WSL interpola el PATH de Windows (con espacios de `Program Files`) dentro del `export` sin comillas → `bash: not a valid identifier` y el MCP server nunca arranca. Path absoluto vía `$HOME` citado es inmune. La forma `bash -lc` también funciona una vez arreglado el PATH del punto 1, pero path absoluto es lo más robusto.

### 3. Plugin de detección (ya incluido en la config global)
`~/.config/opencode/plugins/ripwire-autconfig.ts` está registrado en `opencode.jsonc` (`"plugin"` array). En cada arranque:
- Detecta ripwire (nativo o WSL) con `spawn` sin shell (cmd.exe rompe el quoting si el PATH de Windows tiene espacios)
- Publica `RIPWIRE_AVAILABLE`, `RIPWIRE_METHOD`, `RIPWIRE_BIN`, `RIPWIRE_VERSION` como env vars
- Inyecta guidance compacta al agente una vez por sesión (`experimental.chat.system.transform`) para que use ripwire antes de grep+read a ciegas
- Si no está instalado, loggea el comando de instalación en el log de la app (fail-open)

### 4. REGLA ANTI-WRAPPER — WSL-ONLY (no la saltes)
**ripwire vive en WSL. NO se usa ni se instala nativo en Windows.** El plugin incluye un guard (`tool.execute.before`) que **bloquea**:
- Crear `ripwire.cmd` / `ripwire.ps1` / `ripwire.exe` / `ripwire.bat` en el home de Windows (vía tools de escritura o vía shell redirects / `Set-Content` / `Copy-Item`)
- Ejecutar esos wrappers

**Por qué:** un agente que detecta que "algo está mal" con la vía WSL tiende a programar un wrapper ps1/cmd para hacerlo funcional sin WSL — eso duplica la instalación, cambia el flujo y la lógica, y puede pisar la config MCP. La vía correcta es siempre:
```bash
wsl bash -c 'exec "$HOME/.local/bin/ripwire" <dir> --for="<task>"'
# o el MCP server "ripwire" (registrado en opencode.jsonc)
```
Si la vía WSL falla, se reporta el error exacto al usuario — no se inventan workarounds.

## Uso

### CLI directo (recomendado, más barato)
```bash
# Orientarse en el repo
ripwire . --for="orient myself in this project"

# Encontrar dónde se maneja algo
ripwire . --for="user authentication"

# Blast radius de un cambio
ripwire . --impact=FunctionName

# Qué tests correr
ripwire . --situ

# Stack trace / build error
ripwire . --from-trace=error.log
```

### MCP server (contexto warm entre calls)
El MCP server se inicia automáticamente cuando opencode lo necesita. Da acceso a 31 verbs:
- `analyze`, `find_symbol`, `find_referencing_symbols`, `grep`
- `for`, `pack_task`, `impact`, `uses`, `callers`
- `quality_delta`, `test_gate`, `edit_check`
- `replace_symbol_body`, `insert_before_symbol`, `insert_after_symbol`

## Verificar instalación
```bash
ripwire --version          # Debe mostrar: ripwire 0.6.0
ripwire . --doctor         # Verifica binario, grammars, cache, git
ripwire . --for="test"     # Debe producir output XML con rankings
```
Y el handshake MCP (lo que opencode ejecuta al conectar):
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  | wsl bash -c 'exec "$HOME/.local/bin/ripwire" --mcp'
# Debe responder JSON con "serverInfo":{"name":"ripwire",...}
```

## En AGENTS.md (reglas para el agente)
Agregar al AGENTS.md del proyecto:
```markdown
## ripwire — deterministic codebase maps
Reach for it BEFORE blind grep + whole-file reads.
- Orient on a task: `ripwire <dir> --for="<task>"`
- One task: `--pack-task="<task>"`
- Blast radius: `--impact=SYM` + `--uses=SYM`
- Before writing new code: `--exemplar="<what you're writing>"`
- Before calling done: `--quality-delta` then `--test-gate`
```

## Archivos creados por ripwire en el repo
- `.ripwire_config` — configuración del proyecto
- `.ripwire_notes` — notas del agente
- `.ripwire_quality_baseline` — baseline de calidad
- `.ripwire_quality_acks` — acks de calidad

## Upgrade
```bash
RIPWIRE_REPO=redhat-et/ripwire RIPWIRE_INSTALL_YES=1 bash -c "$(curl -fsSL https://raw.githubusercontent.com/redhat-et/ripwire/main/scripts/install.sh)"
```

## Uninstall
```bash
rm -f ~/.local/bin/ripwire
rm -rf ~/.local/share/ripwire
# y quitar la entrada mcp.ripwire + plugin de ~/.config/opencode/opencode.jsonc
```
