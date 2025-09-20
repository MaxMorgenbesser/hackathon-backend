from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestHistoryRoutes:
    def test_get_history(self):
        response = client.get("/history")
        assert response.status_code == 200
        json_response = response.json()
        print(json_response)