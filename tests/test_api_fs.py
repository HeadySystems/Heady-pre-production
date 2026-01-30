import os
from fastapi.testclient import TestClient
from src.heady_project.api import app

client = TestClient(app)
TOKEN = "default_insecure_token"
HEADERS = {"X-Admin-Token": TOKEN}

def test_file_lifecycle():
    # 1. Save a new file
    test_file = "test_data_temp.txt"
    content = "Hello World"
    response = client.post("/api/files", json={"path": test_file, "content": content}, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 2. Read the file
    response = client.get(f"/api/files/{test_file}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"content": content}

    # 3. List files and check it exists
    response = client.get("/api/files", headers=HEADERS)
    assert response.status_code == 200
    files = response.json()["files"]
    assert test_file in files

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

def test_path_traversal_protection():
    # Try to access /etc/passwd or something outside
    response = client.get("/api/files/../../../../etc/passwd", headers=HEADERS)
    # 403 is denied, 404 means URL didn't match (also safe from disclosure)
    assert response.status_code in [403, 404]

def test_save_outside_root():
    response = client.post("/api/files", json={"path": "../outside.txt", "content": "bad"}, headers=HEADERS)
    assert response.status_code == 403
