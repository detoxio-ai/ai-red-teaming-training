#!/bin/bash

# Exit immediately if any command fails
set -e

# Define paths
LABS_DIR="$HOME/labs"
REPO_URL="https://github.com/vxcontrol/pentagi.git"
REPO_DIR="$LABS_DIR/pentagi"
SECRETS_DIR="$HOME/.secrets"
OPENAI_FILE="$SECRETS_DIR/OPENAI_API_KEY.txt"
ENV_TEMPLATE=".env.example"
ENV_FILE=".env"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Create labs directory
mkdir -p "$LABS_DIR"
cd "$LABS_DIR"

# Clone Pentagi repo if not already present
if [ ! -d "$REPO_DIR" ]; then
  echo "Cloning Pentagi repository..."
  git clone "$REPO_URL"
else
  echo "Repository already exists at $REPO_DIR"
fi

cd "$REPO_DIR"

# Ensure .env.template exists
if [ ! -f "$ENV_TEMPLATE" ]; then
  echo "❌ ERROR: $ENV_TEMPLATE not found in $REPO_DIR"
  exit 1
fi

# Copy .env.template to .env
echo "Copying $ENV_TEMPLATE to $ENV_FILE..."
cp "$ENV_TEMPLATE" "$ENV_FILE"

# Inject OpenAI API key
if [ -f "$OPENAI_FILE" ]; then
  OPENAI_KEY=$(cat "$OPENAI_FILE")
  if grep -q "^OPENAI_API_KEY=" "$ENV_FILE"; then
    sed -i.bak "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=${OPENAI_KEY}|" "$ENV_FILE"
  else
    echo "OPENAI_API_KEY=${OPENAI_KEY}" >> "$ENV_FILE"
  fi
  echo "✅ OpenAI key inserted into $ENV_FILE"
else
  echo "❌ ERROR: OpenAI key file not found at $OPENAI_FILE"
  exit 1
fi

# Replace 127.0.0.1 with 0.0.0.0 in docker-compose.yml
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
  sed -i.bak 's/127\.0\.0\.1/0.0.0.0/g' "$DOCKER_COMPOSE_FILE"
  echo "🔧 Replaced 127.0.0.1 with 0.0.0.0 in $DOCKER_COMPOSE_FILE"
else
  echo "⚠️ WARNING: $DOCKER_COMPOSE_FILE not found; skipping IP replacement."
fi

# Start and stop docker to pull and cache images
echo "📦 Starting containers to preload images..."
docker compose up -d

echo "🧹 Shutting down containers (images cached)..."
docker compose down

echo "✅ Pentagi setup complete in: $REPO_DIR"
