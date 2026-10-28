#!/usr/bin/env bash
# scripts/stop_services.sh - Safely stop containers or background services
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "[*] Stopping docker compose services..."
cd "$ROOT_DIR"
if docker compose ps -q cassandra 2>/dev/null | grep -q .; then
    docker compose stop cassandra
    echo "[+] Cassandra container stopped."
else
    echo "[i] Cassandra is not running inside docker compose."
    if systemctl is-active --quiet cassandra; then
        echo "[i] Host Cassandra service is managed by systemd: sudo systemctl stop cassandra"
    fi
fi
echo "[+] Done."
