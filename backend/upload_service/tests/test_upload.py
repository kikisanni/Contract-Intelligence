import os
import pytest
from fastapi.testclient import TestClient
from upload_service.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_contract(tmp_path):
    # Create a dummy file
    dummy_file = tmp_path / "contract.pdf"
    dummy_file.write_text("Sample contract content")

    with open(dummy_file, "rb") as f:
        response = client.post("/upload", files={"file": ("contract.pdf", f, "application/pdf")})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["filename"] == "contract.pdf"
    assert data["file_url"]  # should point to local path or s3
