#!/usr/bin/env bash
# scripts/check_environment.sh - Inspect local runtime stack
set -euo pipefail

echo "=========================================="
echo " AirIQ - Environment "
echo "=========================================="

echo "[*] Host: $(uname -s) $(uname -r) ($(uname -m))"
echo "[*] Python 3: $(python3 --version 2>&1)"
echo "[*] Virtual Env: $(if [ -d ".venv" ]; then echo "Present (.venv)"; else echo "Missing"; fi)"
echo "[*] Java: $(java -version 2>&1 | head -n 1)"
echo "[*] Node.js: $(node -v 2>&1)"
echo "[*] npm: $(npm -v 2>&1)"
echo "[*] Docker: $(docker --version 2>&1)"
echo "[*] Cassandra Native Port (9042): $(if ss -tuln | grep -q ':9042 '; then echo "Listening (Active)"; else echo "Not listening"; fi)"

echo ""
echo "[*] Checking Python Virtual Environment Packages..."
if [ -f ".venv/bin/python" ]; then
    .venv/bin/python -c "
import pyspark, cassandra, fastapi, uvicorn, pandas, numpy, sklearn
print('    -> PySpark:', pyspark.__version__)
print('    -> Cassandra Driver:', cassandra.__version__)
print('    -> FastAPI:', fastapi.__version__)
print('    -> Pandas:', pandas.__version__)
print('    -> Scikit-learn:', sklearn.__version__)
"
else
    echo "    [!] Virtualenv .venv not found. Run python3 -m venv .venv"
fi
echo "=========================================="
