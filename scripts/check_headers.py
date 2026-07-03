import asyncio
import httpx
from fastapi.testclient import TestClient
from backend.app.main import create_app

app = create_app()
client = TestClient(app)

response = client.get("/api/v1/health")
print("Response Status:", response.status_code)
print("Response Headers:")
for k, v in response.headers.items():
    if k.lower().startswith("content-security-policy") or k.lower().startswith("x-") or k.lower() == "referrer-policy":
        print(f"{k}: {v}")
