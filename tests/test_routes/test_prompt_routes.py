from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

class TestPromptRoutes:

    def test_update_prompt(self):
        response = client.put("/prompt", json={"id": 123, "coupons": True, "Feedback": True, "Newsletters": True, "exclusions": "test"})
        assert response.status_code == 200
        json_response = response.json()
        print(json_response)
        # assert response.json() == {"id": 123, "coupons": True, "Feedback": True, "Newsletters": True, "exclusions": "test"}

    def test_get_prompt(self):
        response = client.get("/prompt")
        assert response.status_code == 200
        json_response = response.json()
        print(json_response)
        # assert response.json() == {"id": 123, "coupons": True, "Feedback": True, "Newsletters": True, "exclusions": "test"}