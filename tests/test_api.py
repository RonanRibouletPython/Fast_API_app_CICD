from fastapi.testclient import TestClient
from app.api.main import app  # Import from the correct package

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}