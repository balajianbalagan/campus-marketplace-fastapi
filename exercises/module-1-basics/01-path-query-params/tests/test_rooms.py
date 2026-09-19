import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import app
    return TestClient(app)


def test_get_room(client):
    r = client.get("/buildings/1/rooms/101")
    assert r.status_code == 200
    assert r.json() == {"building_id": 1, "room_number": "101"}


def test_building_id_must_be_positive(client):
    r = client.get("/buildings/0/rooms/101")
    assert r.status_code == 422


def test_list_rooms_default(client):
    r = client.get("/rooms")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_list_rooms_filters(client):
    r = client.get("/rooms", params={"capacity_min": 20, "has_projector": True})
    numbers = {room["room_number"] for room in r.json()}
    assert numbers == {"101", "201"}


def test_limit_capped_at_50(client):
    r = client.get("/rooms", params={"limit": 999})
    assert r.status_code == 422
