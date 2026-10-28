#!/usr/bin/env bash
# scripts/init_cassandra.sh - Idempotently apply Cassandra keyspace and tables
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SCHEMA_FILE="$ROOT_DIR/cassandra/schema.cql"

echo "[*] Applying Cassandra schema from $SCHEMA_FILE..."

if command -v cqlsh >/dev/null 2>&1; then
    cqlsh 127.0.0.1 9042 -f "$SCHEMA_FILE"
elif docker compose ps -q cassandra 2>/dev/null | grep -q .; then
    docker compose exec -T cassandra cqlsh -f /docker-entrypoint-initdb.d/schema.cql 127.0.0.1 9042
else
    echo "[-] Error: neither local cqlsh nor cassandra container found."
    exit 1
fi

echo "[+] Schema applied successfully. Verifying tables:"
if command -v cqlsh >/dev/null 2>&1; then
    cqlsh 127.0.0.1 9042 -e "DESCRIBE KEYSPACE airbnb_intelligence;" | grep "CREATE TABLE"
fi
echo "[+] Cassandra initialization complete."
