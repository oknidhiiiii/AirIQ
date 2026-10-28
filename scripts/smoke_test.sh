#!/usr/bin/env bash
# scripts/smoke_test.sh - End-to-end verification of PySpark, Cassandra, FastAPI, and Vite build
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo " AirIQ - Smoke Tests  "
echo "=========================================="

echo "[1/4] Running Backend pytest Suite (FastAPI, PySpark, Cassandra Drivers)..."
cd "$ROOT_DIR"
.venv/bin/pytest tests/test_backend.py -v

echo ""
echo "[2/4] Testing Standalone PySpark Session Aggregation..."
export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
.venv/bin/python - << 'EOF'
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Smoke").master("local[1]").config("spark.driver.bindAddress", "127.0.0.1").config("spark.ui.enabled", "false").getOrCreate()
df = spark.createDataFrame([(1, "listing_a", 100.0), (2, "listing_b", 200.0)], ["id", "name", "price"])
avg_p = df.agg({"price": "avg"}).collect()[0][0]
print(f"      [+] Spark Aggregation Success: Average Price = {avg_p}")
spark.stop()
EOF

echo ""
echo "[3/4] Verifying Cassandra Keyspace and Table Queries..."
.venv/bin/python - << 'EOF'
from cassandra.cluster import Cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('airbnb_intelligence')
rows = session.execute("SELECT table_name FROM system_schema.tables WHERE keyspace_name='airbnb_intelligence'")
tables = [r.table_name for r in rows]
print(f"      [+] Found Cassandra Tables: {tables}")
cluster.shutdown()
EOF

echo ""
echo "[4/4] Verifying Frontend React + Vite Production Build..."
cd "$ROOT_DIR/frontend"
npm run build

echo ""
echo "=========================================="
echo "[SUCCESS] All Environment Smoke Tests Passed!"
echo "=========================================="
