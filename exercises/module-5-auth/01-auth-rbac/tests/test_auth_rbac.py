import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import USERS, app
    USERS.clear()
    return TestClient(app)


def _register_and_login(client, username, password, role="member"):
    client.post("/register", json={"username": username, "password": password, "role": role})
    r = client.post("/login", data={"username": username, "password": password})
    return r.json()["access_token"]


def test_register_and_login(client):
    r = client.post("/register", json={"username": "sam", "password": "pw12345"})
    assert r.status_code == 201
    assert r.json() == {"username": "sam", "role": "member"}

    r = client.post("/login", data={"username": "sam", "password": "pw12345"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_duplicate_register_400(client):
    client.post("/register", json={"username": "pat", "password": "pw12345"})
    r = client.post("/register", json={"username": "pat", "password": "pw12345"})
    assert r.status_code == 400


def test_member_cannot_spend_funds(client):
    token = _register_and_login(client, "member1", "pw12345", role="member")
    r = client.delete("/club-funds/50", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_officer_can_spend_funds(client):
    token = _register_and_login(client, "officer1", "pw12345", role="officer")
    r = client.delete("/club-funds/50", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == {"approved_by": "officer1", "amount": 50}


def test_no_token_401(client):
    r = client.delete("/club-funds/50")
    assert r.status_code == 401
