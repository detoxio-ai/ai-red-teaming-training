#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/dtx-validate.log"
echo "🔍 DTX Validation Log - $(date)" > "$LOG"
echo "==================================" >> "$LOG"

# === Helper Functions ===
check_tool() {
  local name="$1"
  local cmd="$2"
  echo -n "Checking $name... " >> "$LOG"
  if command -v "$cmd" &>/dev/null; then
    echo "✅ Found ($($cmd --version 2>&1 | head -n 1))" >> "$LOG"
  else
    echo "❌ NOT FOUND" >> "$LOG"
  fi
}

check_url() {
  local name="$1"
  local url="$2"
  echo -n "🌐 $name [$url]... " >> "$LOG"
  for i in {1..5}; do
    if curl -sk --head --fail "$url" >/dev/null; then
      echo "✅ Reachable" >> "$LOG"
      return
    else
      echo -n "." >> "$LOG"
      sleep 10
    fi
  done
  echo "❌ NOT reachable after 5 tries" >> "$LOG"
}


# === External IP ===
echo -e "\n🌍 External Network Info" >> "$LOG"
EXTERNAL_IP=$(curl -s ifconfig.io || echo "Unavailable")
echo "🌐 External IP: $EXTERNAL_IP" >> "$LOG"

# === Secrets ===
echo -e "\n🔐 Validating API keys..." >> "$LOG"
for key in ANTHROPIC_API_KEY.txt GROQ_API_KEY.txt OPENAI_API_KEY.txt; do
  if [[ -f "$HOME/.secrets/$key" ]]; then
    echo "✅ Found $key" >> "$LOG"
  else
    echo "❌ Missing $key" >> "$LOG"
  fi
done

# === CLI Tools ===
echo -e "\n🧰 Validating core tools..." >> "$LOG"
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
echo -e "\n🚀 Starting Docker labs..." >> "$LOG"

cd "$HOME/labs/pentagi" && docker compose up -d >> "$LOG" 2>&1 && echo "✅ Pentagi started" >> "$LOG" || echo "❌ Pentagi failed" >> "$LOG"
cd "$HOME/labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab" && docker compose up -d >> "$LOG" 2>&1 && echo "✅ AI Demo Agents started" >> "$LOG" || echo "❌ AI Demo Agents failed" >> "$LOG"

# === Start Promptfoo and Autogen Studio ===
echo -e "\n🚀 Starting Promptfoo and Autogen Studio (no tmux)..." >> "$LOG"

promptfoo dev > /dev/null 2>&1 &
PROMPTFOO_PID=$!
echo "✅ Promptfoo started with PID $PROMPTFOO_PID" >> "$LOG"

autogenstudio ui --port 18081 > /dev/null 2>&1 &
AUTOGEN_PID=$!
echo "✅ Autogen Studio started with PID $AUTOGEN_PID" >> "$LOG"

sleep 10

# === Port Checks ===
echo -e "\n🌐 Checking port accessibility..." >> "$LOG"

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
  check_url "$name (localhost)" "$url"
  if [[ "$EXTERNAL_IP" != "Unavailable" ]]; then
    external_url="${url/localhost/$EXTERNAL_IP}"
    check_url "$name (external)" "$external_url"
  fi
done

# === Stop Docker Services ===
echo -e "\n🛑 Stopping Docker labs..." >> "$LOG"
cd "$HOME/labs/pentagi" && docker compose down >> "$LOG" 2>&1 && echo "✅ Pentagi stopped" >> "$LOG"
cd "$HOME/labs/ai-red-teaming-training/lab/vuln_apps/dtx_vuln_app_lab" && docker compose down >> "$LOG" 2>&1 && echo "✅ AI Demo Agents stopped" >> "$LOG"

# === Stop Background UIs ===
echo -e "\n🛑 Stopping background web UIs..." >> "$LOG"

if ps -p $PROMPTFOO_PID > /dev/null 2>&1; then
  kill $PROMPTFOO_PID && echo "✅ Promptfoo stopped (PID $PROMPTFOO_PID)" >> "$LOG"
else
  echo "⚠️ Promptfoo process not found." >> "$LOG"
fi

if ps -p $AUTOGEN_PID > /dev/null 2>&1; then
  kill $AUTOGEN_PID && echo "✅ Autogen Studio stopped (PID $AUTOGEN_PID)" >> "$LOG"
else
  echo "⚠️ Autogen Studio process not found." >> "$LOG"
fi

# === Done ===
echo -e "\n✅ DTX Validation complete. Log saved to $LOG"
