# AirIQ — Airbnb Price Intelligence Platform (BDA)

A distributed Big Data Analytics platform for multi-city Airbnb price intelligence, spatial exploration, and MLlib-driven price prediction.

## Architecture

- **Distributed Data Processing:** Apache Spark & PySpark (`pyspark 4.2.0`)
- **NoSQL Storage:** Apache Cassandra 4.1 (`airbnb_intelligence` keyspace)
- **Machine Learning Engine:** PySpark MLlib (`RandomForestRegressor` pipeline)
- **Backend API:** FastAPI (`0.162.0`) + Uvicorn with async ASGI architecture
- **Frontend Client:** React 19 + Vite 8 + Tailwind CSS + React Router + Recharts + Leaflet
- **Isolation:** Local Python virtual environment (`.venv`) & Docker Compose for Cassandra

---

## Directory Structure

```text
airbnb-price-intelligence/
├── data/
│   ├── raw/                 # Downloaded Airbnb listing CSV datasets (gitignored)
│   ├── processed/           # Processed parquet/cleansed partitions (gitignored)
│   └── README.md
├── notebooks/               # EDA and prototype exploration notebooks
├── spark/                   # PySpark ETL scripts and MLlib feature pipeline definitions
├── cassandra/
│   └── schema.cql           # Idempotent keyspace and table DDL with partition keys
├── models/                  # Serialized Spark MLlib Random Forest model artifacts (gitignored)
├── backend/
│   ├── main.py              # FastAPI application exposing health & REST endpoints
│   ├── requirements.txt     # Backend-specific locked dependencies
│   └── README.md
├── frontend/                # React + Vite application shell with Tailwind & charts
├── scripts/
│   ├── check_environment.sh # Audit system tools and virtualenv packages
│   ├── start_services.sh    # Verify/start Cassandra and database schema
│   ├── stop_services.sh     # Safely stop running Docker services
│   ├── init_cassandra.sh    # Idempotent CQL migration runner
│   └── smoke_test.sh        # End-to-end environment verification suite
├── tests/
│   └── test_backend.py      # Pytest async test suite for FastAPI & dependencies
├── .env.example             # Safe template for local environment variables
├── .gitignore               # Strict ignore rules protecting models, secrets & data
├── docker-compose.yml       # Cassandra 4.1 container configuration
├── requirements.txt         # Root frozen dependencies
└── README.md                # System documentation
```

---

## Prerequisites

- **OS:** Kali Linux Rolling / Debian-based x86_64
- **Python:** Python 3.14+ (or compatible 3.11–3.14)
- **Java:** OpenJDK 21 (`/usr/lib/jvm/java-21-openjdk-amd64`)
- **Node.js:** Node v24+ & npm 11+
- **Docker & Docker Compose:** Docker 28+

---

## Environment Setup Instructions

### 1. Python Virtual Environment Setup

```bash
# Navigate to the project root
cd /home/adityap/Desktop/PR/BDALAB/airbnb-price-intelligence

# Create virtualenv if not already created
python3 -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

---

## Running and Managing Services

### 1. Apache Cassandra

You can manage Cassandra via the provided automated scripts or Docker Compose directly:

- **Start Cassandra & Initialize Schema:**
  ```bash
  ./scripts/start_services.sh
  ```
  *Or manually via Docker Compose:*
  ```bash
  docker compose up -d cassandra
  ./scripts/init_cassandra.sh
  ```

- **Stop Cassandra:**
  ```bash
  ./scripts/stop_services.sh
  ```

- **Inspect Keyspace Schema:**
  ```bash
  cqlsh 127.0.0.1 9042 -e "DESCRIBE KEYSPACE airbnb_intelligence;"
  ```

### 2. FastAPI Backend

```bash
source .venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Endpoints available:
- `http://127.0.0.1:8000/health` (Application health)
- `http://127.0.0.1:8000/health/spark` (SparkSession probe & test aggregation)
- `http://127.0.0.1:8000/health/cassandra` (Cassandra cluster & keyspace status)
- `http://127.0.0.1:8000/api/v1/cities` (Configured city targets)
- `http://127.0.0.1:8000/docs` (Swagger UI when `DEBUG=True`)

### 3. React + Vite Frontend

```bash
cd frontend
npm run dev
```

Visit the dashboard at `http://127.0.0.1:5173`.

---

## Running Verification & Smoke Tests

Execute the automated smoke test script to verify all layers:

```bash
./scripts/smoke_test.sh
```

Or run individual component tests:

```bash
# Backend pytest suite (FastAPI, Spark, Cassandra integration)
.venv/bin/pytest tests/test_backend.py -v

# Frontend production build verification
cd frontend && npm run build
```

---

## Troubleshooting Guide

### 1. Java & Spark Compatibility
- **Issue:** Spark complains about missing `JAVA_HOME` or Java incubator modules.
- **Fix:** Explicitly export Java 21:
  ```bash
  export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
  export PATH="$JAVA_HOME/bin:$PATH"
  ```

### 2. Cassandra Native Transport Connection (Port 9042)
- **Issue:** `NoHostAvailable` or connection refused on `127.0.0.1:9042`.
- **Fix:** Cassandra takes 20–40 seconds on cold start to initialize native transport. Check status with:
  ```bash
  nodetool status
  # or check listening ports
  ss -tuln | grep 9042
  ```

### 3. Docker Permissions
- **Issue:** `permission denied while trying to connect to the Docker daemon socket`.
- **Fix:** Ensure your user belongs to the `docker` group (`groups`), or start with appropriate permissions.
