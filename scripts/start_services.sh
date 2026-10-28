#!/usr/bin/env bash
# scripts/start_services.sh - Start Cassandra and background services
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "[*] Checking Apache Cassandra on port 9042..."
if ss -tuln | grep -q ':9042 '; then
    echo "[+] Cassandra is already running and listening on port 9042."
else
    echo "[*] Starting Cassandra via Docker Compose..."
    cd "$ROOT_DIR"
    docker compose up -d cassandra
    echo "[*] Waiting for Cassandra native transport to be ready on 127.0.0.1:9042..."
    until ss -tuln | grep -q ':9042 '; do
        sleep 2
    done
    echo "[+] Cassandra container is active and listening on port 9042."
fi

echo "[*] Ensuring Cassandra schema is initialized..."
"$SCRIPT_DIR/init_cassandra.sh"
echo "[+] All services ready."
