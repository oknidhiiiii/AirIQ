import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from main import app

@pytest.mark.anyio
async def test_app_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "fastapi-backend"

@pytest.mark.anyio
async def test_cassandra_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health/cassandra")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "airbnb_intelligence" in data["keyspaces"]

@pytest.mark.anyio
async def test_spark_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health/spark")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "apache-spark"

@pytest.mark.anyio
async def test_cities():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/cities")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "configuration_placeholder"
    assert len(data["cities"]) > 0
