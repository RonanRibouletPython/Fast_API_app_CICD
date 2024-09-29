from fastapi.testclient import TestClient
from app.api.main import app  # Import from the correct package

client = TestClient(app)
