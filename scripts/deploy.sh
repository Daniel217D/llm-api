#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[deploy] pulling latest"
git pull --ff-only origin main

echo "[deploy] restart"
docker compose pull || true
docker compose up -d --build

echo "[deploy] cleanup"
docker image prune -f
