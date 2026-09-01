#!/usr/bin/env bash
set -euo pipefail

# Determine destination folder from .env.dev or argument or default
DEST="${1:-}"
if [ -z "$DEST" ]; then
  if [ -f ".env.dev" ]; then
    DEST=$(grep -E "^C4_DESTINATION=" .env.dev | cut -d '=' -f2- | tr -d '"' | tr -d "'" || true)
  fi
fi

if [ -z "$DEST" ]; then
  DEST="docs/architecture"
fi

PORT="${PORT:-8080}"
DEST_PATH="$(pwd)/$DEST"

mkdir -p "$DEST_PATH"

echo "Launching Structurizr Local..."
echo "  URL: http://localhost:$PORT"
echo "  Workspace directory: $DEST_PATH"

docker pull structurizr/structurizr
docker run -it --rm \
  -p "$PORT:8080" \
  -v "$DEST_PATH:/usr/local/structurizr" \
  structurizr/structurizr local
