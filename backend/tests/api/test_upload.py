import io

from fastapi.testclient import TestClient

from backend.app.core.config import settings


def test_upload_success(client: TestClient) -> None:
    """Test successful upload of a valid CSV."""
    csv_content = b"header1,header2\n1,2\n3,4"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}

    response = client.post(f"{settings.api_v1_prefix}/upload", files=files)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Dataset uploaded successfully"
    assert "dataset_id" in data["data"]
    assert data["data"]["filename"] == "test.csv"
    assert data["data"]["size_bytes"] > 0


def test_upload_invalid_extension(client: TestClient) -> None:
    """Test uploading a file with an invalid extension."""
    txt_content = b"some text content"
    files = {"file": ("test.txt", io.BytesIO(txt_content), "text/plain")}

    response = client.post(f"{settings.api_v1_prefix}/upload", files=files)
    assert response.status_code == 422

    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Unsupported MIME type" in data["error"]["details"]
