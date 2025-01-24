from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


VALID_PAYLOAD = {
    "food_image_url": "data:image/jpeg;base64,valid_base64_string==",
    "food_description_expected": "100g de frango, 200g de arroz, 100g de feijão",
}


def test_valid_request():
    res = client.post("/diet", json=VALID_PAYLOAD)
    assert res.status_code == status.HTTP_200_OK
    assert "Nice! You're eating" in res.json()["message"]
