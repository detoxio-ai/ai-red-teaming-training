#!/usr/bin/env bash
set -euo pipefail

# === Parse arguments ===
LOG_FILE=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --log)
      LOG_FILE="$2"
      shift 2
      ;;
    *)
      echo "❌ Unknown option: $1"
      echo "Usage: $0 [--log /path/to/logfile]"
      exit 1
      ;;
  esac
done

# === Default log file ===
if [[ -z "$LOG_FILE" ]]; then
  LOG_FILE="$HOME/dtx-validate.log"
fi

# === Logging helper ===
log() {
  echo "$1"
  echo "$1" >> "$LOG_FILE"
}

# === Start log ===
log "🔍 DTX Validation Log - $(date)"
log "=================================="

# === Helper Functions ===
check_tool() {
  local name="$1"
  local cmd="$2"
  if command -v "$cmd" &>/dev/null; then
    local version
    version="$($cmd --version 2>&1 | head -n 1 || true)"
    log "✅ $name is installed: $version"
  else
    log "❌ $name is NOT installed"
  fi
}

check_url() {
  local name="$1"
  local url="$2"
  log "🌐 $name [$url]..."
  for i in {1..5}; do
    if curl -sk --head --fail "$url" >/dev/null; then
      log "✅ $name reachable at $url"
      return 0
    else
      sleep 10
    fi
  done
  log "❌ $name not reachable after 5 tries ($url)"
  return 1
}


# === External IP ===
log ""
log "🌍 External Network Info"
EXTERNAL_IP=$(curl -s ifconfig.io || echo "Unavailable")
log "🌐 External IP: $EXTERNAL_IP"

# === Secrets ===
log ""
log "🔐 Validating API keys..."
for key in ANTHROPIC_API_KEY.txt GROQ_API_KEY.txt OPENAI_API_KEY.txt; do
  if [[ -f "$HOME/.secrets/$key" ]]; then
    log "✅ Found $key"
  else
    log "❌ Missing $key"
  fi
done

# === CLI Tools ===
log ""
log "🧰 Validating core tools..."
check_tool "Docker" docker
check_tool "Git" git
check_tool "curl" curl
check_tool "Python (uv)" python3
check_tool "Node.js" node
check_tool "npm" npm
check_tool "Go" go
check_tool "asdf" asdf
check_tool "uv" uv
check_tool "llm CLI" llm
check_tool "Nmap" nmap
check_tool "Metasploit" msfconsole
check_tool "Ollama" ollama
check_tool "Promptfoo" promptfoo
check_tool "Garak" garak
check_tool "DTX" dtx
check_tool "Amass" amass
check_tool "Subfinder" subfinder
check_tool "Nuclei" nuclei
check_tool "AutogenStudio" autogenstudio

# === Start Docker Services ===
log ""
log "🚀 Starting Docker labs..."

if cd "$HOME/labs/pentagi"; then
  log "$(docker compose up -d 2>&1)" && log "✅ Pentagi started" || log "❌ Pentagi failed"
else
  log "❌ Pentagi directory not found"
fi

if cd "$HOME/labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab"; then
  log "$(docker compose up -d 2>&1)" && log "✅ AI Demo Agents started" || log "❌ AI Demo Agents failed"
else
  log "❌ DTX vuln lab directory not found"
fi

# === Start Promptfoo and Autogen Studio ===
log ""
log "🚀 Starting Promptfoo and Autogen Studio (no tmux)..."

promptfoo dev > /dev/null 2>&1 &
PROMPTFOO_PID=$!
sleep 1
if ps -p $PROMPTFOO_PID > /dev/null; then
  log "✅ Promptfoo started with PID $PROMPTFOO_PID"
else
  log "❌ Promptfoo failed to start"
fi

autogenstudio ui --port 18081 > /dev/null 2>&1 &
AUTOGEN_PID=$!
sleep 1
if ps -p $AUTOGEN_PID > /dev/null; then
  log "✅ Autogen Studio started with PID $AUTOGEN_PID"
else
  log "❌ Autogen Studio failed to start"
fi

sleep 10

# === Port Checks ===
log ""
log "🌐 Checking port accessibility..."

PORTS=(
  "Pentagi|https://localhost:8443"
  "Chatbot Demo|http://localhost:17860"
  "RAG Demo|http://localhost:17861"
  "Tool Agents Demo|http://localhost:17862"
  "Text2SQL Demo|http://localhost:17863"
  "Promptfoo UI|http://localhost:8080"
  "Autogen Studio|http://localhost:18081"
)

for entry in "${PORTS[@]}"; do
  IFS="|" read -r name url <<< "$entry"
  if check_url "$name (localhost)" "$url"; then
    if [[ "$EXTERNAL_IP" != "Unavailable" ]]; then
      external_url="${url/localhost/$EXTERNAL_IP}"
      check_url "$name (external)" "$external_url"
    fi
  else
    log "⚠️ Skipping external check for $name since internal is not reachable."
  fi
done


# === Stop Docker Services ===
log ""
log "🛑 Stopping Docker labs..."

if cd "$HOME/labs/pentagi"; then
  log "$(docker compose down 2>&1)" && log "✅ Pentagi stopped"
fi

if cd "$HOME/labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab"; then
  log "$(docker compose down 2>&1)" && log "✅ AI Demo Agents stopped"
fi

# === Stop Background UIs ===
log ""
log "🛑 Stopping background web UIs..."

if ps -p $PROMPTFOO_PID > /dev/null 2>&1; then
  kill $PROMPTFOO_PID && log "✅ Promptfoo stopped (PID $PROMPTFOO_PID)"
else
  log "⚠️ Promptfoo process not found."
fi

if ps -p $AUTOGEN_PID > /dev/null 2>&1; then
  kill $AUTOGEN_PID && log "✅ Autogen Studio stopped (PID $AUTOGEN_PID)"
else
  log "⚠️ Autogen Studio process not found."
fi

# === Done ===
log ""
log "✅ DTX Validation complete."
[[ -n "$LOG_FILE" ]] && log "📄 Log saved to $LOG_FILE"
