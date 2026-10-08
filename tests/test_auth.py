from fastapi.testclient import TestClient

# Basic smoke test against the gateway application.
# Full integration tests are intended to run with docker compose.

from gateway.app.main import app

client = TestClient(app)

def test_gateway_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
