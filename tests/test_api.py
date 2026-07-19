"""API endpoint tests."""

from fastapi.testclient import TestClient

from app.core.constants import APP_NAME, APP_VERSION, HealthStatus
from app.main import app


def test_root_returns_system_info() -> None:
    """Root endpoint should return basic system metadata."""
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == APP_NAME
    assert payload["version"] == APP_VERSION
    assert payload["status"] == "running"
    assert "timestamp" in payload
    assert "environment" in payload


def test_health_returns_component_checks() -> None:
    """Health endpoint should return API and database check details."""
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {
        HealthStatus.HEALTHY.value,
        HealthStatus.DEGRADED.value,
        HealthStatus.UNHEALTHY.value,
    }
    assert payload["checks"]["api"]["status"] == "ok"
    assert payload["checks"]["database"]["status"] == "not_configured"
    assert "timestamp" in payload
