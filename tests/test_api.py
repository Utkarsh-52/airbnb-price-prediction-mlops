
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_LISTING = {
    "neighbourhood_group": "Manhattan",
    "neighbourhood": "Midtown",
    "latitude": 40.754,
    "longitude": -73.984,
    "room_type": "Entire home/apt",
    "minimum_nights": 2,
    "number_of_reviews": 10,
    "reviews_per_month": 1.5,
    "calculated_host_listings_count": 1,
    "availability_365": 180,
}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_prediction_endpoint():
    response = client.post("/predict", json=VALID_LISTING)

    assert response.status_code == 200

    data = response.json()

    assert "predicted_price" in data
    assert data["currency"] == "USD"
    assert isinstance(data["predicted_price"], (int, float))
    assert data["predicted_price"] >= 0


def test_invalid_latitude():
    listing = VALID_LISTING.copy()
    listing["latitude"] = 200

    response = client.post("/predict", json=listing)

    assert response.status_code == 422


def test_missing_required_field():
    listing = VALID_LISTING.copy()
    del listing["room_type"]

    response = client.post("/predict", json=listing)

    assert response.status_code == 422
