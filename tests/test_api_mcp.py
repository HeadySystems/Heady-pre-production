from fastapi.testclient import TestClient
from src.heady_project.api import app

client = TestClient(app)
TOKEN = "default_insecure_token"
HEADERS = {"X-Admin-Token": TOKEN}

def test_ai_chat():
    response = client.post("/api/ai/chat", json={
        "messages": [{"role": "user", "content": "Hello"}],
        "context": "some code"
    }, headers=HEADERS)
    assert response.status_code == 200
    assert "reply" in response.json()

def test_mcp_endpoints():
    # List servers
    response = client.get("/api/mcp/servers", headers=HEADERS)
    assert response.status_code == 200
    servers = response.json()["servers"]
    assert isinstance(servers, list)
