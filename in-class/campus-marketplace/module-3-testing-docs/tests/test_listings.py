# TestClient sends requests to the API without starting a separate server process.
from fastapi.testclient import TestClient

# Import the same application object that Uvicorn would serve.
from app.main import app


def test_create_then_read_listing():
    # Create a client that can call the FastAPI routes.
    client = TestClient(app)
    # Send a realistic JSON body to the create endpoint.
    created = client.post("/listings", json={
        "title": "Desk lamp", "description": "Works well", "price_cents": 80000, "seller_name": "Asha"
    })
    # A new database row should return the HTTP "Created" response code.
    assert created.status_code == 201
    # Use the server-assigned id to prove the individual GET route works too.
    assert client.get(f"/listings/{created.json()['id']}").status_code == 200
