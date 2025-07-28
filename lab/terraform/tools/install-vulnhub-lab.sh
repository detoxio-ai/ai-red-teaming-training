#!/bin/bash

# Exit on error
set -e

# Define paths
LABS_DIR="$HOME/labs"
REPO_URL="https://github.com/vulhub/vulhub.git"
REPO_DIR="$LABS_DIR/vulhub"

# Create labs directory
mkdir -p "$LABS_DIR"
cd "$LABS_DIR"

# Clone Vulhub repo if not already present
if [ ! -d "$REPO_DIR" ]; then
  echo "📥 Cloning Vulhub repository..."
  git clone --depth 1 "$REPO_URL"
else
  echo "✅ Repository already exists at $REPO_DIR"
fi

cd "$REPO_DIR"

# List example vulnerable environments
echo -e "\n📂 Example vulnerable environments:"
find . -name docker-compose.yml | sed 's|./||' | sed 's|/docker-compose.yml||' | head -10

echo -e "\n✅ Vulhub setup complete in: $REPO_DIR"
echo "ℹ️ To start a specific environment, navigate to its directory and run: docker compose up -d"
