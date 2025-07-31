#!/bin/bash

# Exit on any error
set -e

# Paths
LABS_DIR="$HOME/labs"
REPO_URL="https://github.com/detoxio-ai/ai-red-teaming-training.git"
REPO_DIR="$LABS_DIR/ai-red-teaming-training"
APP_DIR="$REPO_DIR/lab/vuln_apps/dtx_vuln_app_lab"
SECRETS_DIR="$HOME/.secrets"

# API key files
OPENAI_FILE="$SECRETS_DIR/OPENAI_API_KEY.txt"
GROQ_FILE="$SECRETS_DIR/GROQ_API_KEY.txt"

# Clone repository if needed
mkdir -p "$LABS_DIR"
cd "$LABS_DIR"

if [ ! -d "$REPO_DIR" ]; then
  echo "📦 Cloning Dtx Demo Lab repository..."
  git clone "$REPO_URL"
else
  echo "✅ Repository already exists at $REPO_DIR"
fi

# Navigate to application directory
cd "$APP_DIR"

# Ensure .env.template exists
if [ ! -f ".env.template" ]; then
  echo "❌ ERROR: .env.template not found in $APP_DIR"
  exit 1
fi

# Copy .env.template to .env
echo "📝 Creating .env from template..."
cp .env.template .env

# Helper function to update env vars
update_env_var() {
  VAR_NAME="$1"
  VAR_VALUE="$2"
  if grep -q "^${VAR_NAME}=" .env; then
    sed -i.bak "s|^${VAR_NAME}=.*|${VAR_NAME}=${VAR_VALUE}|" .env
  else
    echo "${VAR_NAME}=${VAR_VALUE}" >> .env
  fi
}

# Inject secrets
echo "🔐 Injecting API keys into .env..."
[ -f "$OPENAI_FILE" ]     && update_env_var "OPENAI_API_KEY"     "$(cat "$OPENAI_FILE")"
[ -f "$GROQ_FILE" ]       && update_env_var "GROQ_API_KEY"       "$(cat "$GROQ_FILE")"

# Start and stop containers to pull images
echo "🐳 Starting Docker containers to preload images..."
docker compose up -d

echo "🛑 Shutting down containers (images cached)..."
docker compose down

echo "✅ Setup complete. Images are now preloaded and environment is ready."

