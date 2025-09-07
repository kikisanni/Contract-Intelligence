from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_upload_invalid_file():
    response = client.post("/upload", files={"file": ("test.txt", b"dummy")})
    assert response.status_code == 400

def test_upload_pdf():
    response = client.post("/upload", files={"file": ("contract.pdf", b"fake-pdf-data")})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["filename"] == "contract.pdf"
