from fastapi.testclient import TestClient
from upload_service.main import app

client = TestClient(app)

def test_list_contracts_empty():
    response = client.get("/contracts")
    assert response.status_code == 200
    assert response.json() == []
