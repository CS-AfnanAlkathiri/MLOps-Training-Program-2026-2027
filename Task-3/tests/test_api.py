from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_endpoint():
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "olist-late-delivery"
    assert data["model_version"] == 1
    assert data["alias"] == "champion"


def test_predict_endpoint():
    payload = {
        "order_purchase_timestamp": "2018-06-21T08:29:29",
        "order_estimated_delivery_date": "2018-07-17T00:00:00",
        "customer_state": "MG",
        "seller_state": "SP",
        "item_count": 1,
        "total_price": 46.0,
        "total_freight_value": 18.42,
        "unique_products": 1,
        "unique_sellers": 1,
        "payment_count": 2,
        "total_payment_value": 64.42,
        "max_installments": 1,
        "payment_type_count": 2,
        "distance_km": 635.2422079475232,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in ["late", "on_time"]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["model_version"] == 1
