from fastapi.testclient import TestClient

from app.main import app


def test_create_then_read_listing():
    client = TestClient(app)
    created = client.post("/listings", json={
        "title": "Desk lamp", "description": "Works well", "price_cents": 80000, "seller_name": "Asha"
    })
    assert created.status_code == 201
    assert client.get(f"/listings/{created.json()['id']}").status_code == 200
