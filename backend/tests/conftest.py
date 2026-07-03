import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client() -> TestClient:
    """Returns a FastAPI TestClient."""
    return TestClient(app)
