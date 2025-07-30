#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
REPO_URL="https://github.com/ghostsecurity/reaper.git"
CLONE_DIR="${1:-$HOME/labs/reaper}"
OPENAI_KEY_FILE="$HOME/.secrets/OPENAI_API_KEY.txt"

# --- Ports (customize if needed) ---
PORT=18000
PROXY_PORT=28080

# --- Validate OpenAI Key ---
if [[ ! -f "$OPENAI_KEY_FILE" ]]; then
  echo "❌ Missing OpenAI API key file at: $OPENAI_KEY_FILE"
  exit 1
fi
OPENAI_API_KEY=$(< "$OPENAI_KEY_FILE")

# --- Clone the repo if needed ---
if [[ ! -d "$CLONE_DIR" ]]; then
  echo "📥 Cloning Reaper repo into $CLONE_DIR..."
  git clone --depth=1 "$REPO_URL" "$CLONE_DIR"
fi

cd "$CLONE_DIR"

# --- Generate .env file ---
echo "📝 Writing .env file..."
cat > .env <<EOF
COMPOSE_PROJECT_NAME=reaper
ENV=development
HOST=0.0.0.0
PORT=8000
PROXY_PORT=8080
OPENAI_API_KEY=${OPENAI_API_KEY}
EOF

# --- Generate docker-compose.yml file ---
echo "📄 Writing docker-compose.yml with correct port mappings..."
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  reaper:
    build:
      context: .
      dockerfile: Dockerfile
    env_file: .env
    environment:
      - ENV=docker
      - HOST=0.0.0.0
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
    ports:
      - ${PORT}:8000
      - ${PROXY_PORT}:8080
EOF

# --- Start Reaper ---
echo "🚀 Starting Reaper with Docker Compose..."
docker compose up -d --build
docker compose stop

# --- Done ---
echo "✅ Reaper is running!"
echo "→ Main UI:     http://localhost:${PORT}"
echo "→ Proxy Port:  http://localhost:${PROXY_PORT}"
