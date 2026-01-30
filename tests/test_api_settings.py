from fastapi.testclient import TestClient
from src.heady_project.api import app
import os

client = TestClient(app)
TOKEN = "default_insecure_token"
HEADERS = {"X-Admin-Token": TOKEN}
SETTINGS_FILE = "admin_settings.json"

def test_settings_flow():
    # 1. Get default settings
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)

    response = client.get("/api/settings", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "remote_gpu" in data
    assert data["remote_gpu"]["enabled"] is False

    # 2. Update settings
    new_settings = {
        "remote_gpu": {
            "enabled": True,
            "host": "gpu-node-1",
            "port": 9000,
            "memory_limit": "32GB",
            "use_rdma": True
        }
    }
    response = client.post("/api/settings", json=new_settings, headers=HEADERS)
    assert response.status_code == 200

    # 3. Verify persistence
    response = client.get("/api/settings", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["remote_gpu"]["host"] == "gpu-node-1"
    assert data["remote_gpu"]["use_rdma"] is True

    # Cleanup
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)
