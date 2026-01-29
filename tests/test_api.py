import os
from fastapi.testclient import TestClient
from src.heady_project.api import app

client = TestClient(app)

# Use default token
TOKEN = "default_insecure_token"
HEADERS = {"X-Admin-Token": TOKEN}

def test_read_main_auth():
    response = client.get("/api/files", headers=HEADERS)
    assert response.status_code == 200
    assert "files" in response.json()

def test_read_main_no_auth():
    response = client.get("/api/files")
    assert response.status_code == 422 # Missing header

def test_read_main_bad_auth():
    response = client.get("/api/files", headers={"X-Admin-Token": "wrong"})
    assert response.status_code == 401

def test_trigger_action_audit():
    response = client.post("/api/action", json={"action": "full_audit"}, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"status": "audit_initiated"}

def test_ai_assist():
    response = client.post("/api/ai_assist", json={"context": "code", "prompt": "help"}, headers=HEADERS)
    assert response.status_code == 200
    assert "suggestion" in response.json()
