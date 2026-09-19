# TestClient calls FastAPI in-process, so no separate Uvicorn server is needed.
from fastapi.testclient import TestClient

# Import the app under test and clear its temporary state before testing.
from app.main import app, listings


def test_create_and_read_listing():
    # Start the test with no listings left over from another test.
    listings.clear()
    # Wrap the ASGI app in an HTTP-like test client.
    client = TestClient(app)
    # Send a JSON POST request just as a real frontend would.
    created = client.post("/listings", json={
        "title": "Used Calculus Textbook", "price_cents": 150000, "seller_name": "Priya"
    })
    # A successful create route must return HTTP 201.
    assert created.status_code == 201
    # Read the id returned by POST, then prove the GET route can find that record.
    assert client.get(f"/listings/{created.json()['id']}").status_code == 200
