# Backend Module - AirIQ

FastAPI REST API servicing health checks, Spark jobs triggers, and Cassandra data queries.

## Endpoints

- `GET /health` : Backend service status and version
- `GET /health/spark` : PySpark session initialization and aggregation smoke test
- `GET /health/cassandra` : Cassandra connectivity and keyspace probe
- `GET /api/v1/cities` : Configured target cities vs database status

## Run Locally

```bash
cd backend
source ../.venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
