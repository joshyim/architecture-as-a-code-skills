#!/usr/bin/env bash
set -euo pipefail

DEST="${1:-}"
if [ -z "$DEST" ]; then
  if [ -f ".env.dev" ]; then
    DEST=$(grep -E "^C4_DESTINATION=" .env.dev | cut -d '=' -f2- | tr -d '"' | tr -d "'" || true)
  fi
fi

if [ -z "$DEST" ]; then
  DEST="docs/architecture"
fi

DEST_PATH="$(pwd)/$DEST"
DSL_FILE="$DEST_PATH/workspace.dsl"

if [ ! -f "$DSL_FILE" ]; then
  echo "Error: workspace.dsl not found in $DEST_PATH"
  exit 1
fi

echo "Validating Structurizr DSL in $DEST_PATH..."
docker run --rm \
  -v "$DEST_PATH:/usr/local/structurizr" \
  structurizr/structurizr validate -w workspace.dsl
echo "✓ Structurizr DSL is valid."
