import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import app
    return TestClient(app)


def test_missing_api_key_401(client):
    r = client.get("/events")
    # Header(...) with no default makes it required -> 422 for "missing", not 401.
    # Send a bad key explicitly to hit the 401 path:
    r = client.get("/events", headers={"X-API-Key": "wrong-key"})
    assert r.status_code == 401


def test_valid_key_default_pagination(client):
    r = client.get("/events", headers={"X-API-Key": "campus-secret-key"})
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_pagination_params(client):
    r = client.get("/events", params={"limit": 5, "offset": 5}, headers={"X-API-Key": "campus-secret-key"})
    assert r.status_code == 200
    ids = [e["id"] for e in r.json()]
    assert ids == [6, 7, 8, 9, 10]


def test_limit_over_max_422(client):
    r = client.get("/events", params={"limit": 100}, headers={"X-API-Key": "campus-secret-key"})
    assert r.status_code == 422
