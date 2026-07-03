from fastapi.testclient import TestClient

from backend.app.core.config import settings


def test_health_check(client: TestClient) -> None:
    """Test the basic health check endpoint."""
    response = client.get(f"{settings.api_v1_prefix}/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "System is healthy"
    assert data["data"]["status"] == "OK"
    assert "uptime_seconds" in data["data"]
    assert "memory" in data["data"]
    assert "version" in data
    assert "request_id" in data
    assert "processing_time" in data


def test_ready_check(client: TestClient) -> None:
    response = client.get(f"{settings.api_v1_prefix}/ready")
    assert response.status_code == 200
    assert response.json()["data"] == "READY"


def test_version_check(client: TestClient) -> None:
    response = client.get(f"{settings.api_v1_prefix}/version")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["app_name"] == settings.app_name
    assert data["version"] == settings.version
