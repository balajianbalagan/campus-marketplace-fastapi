import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import app
    return TestClient(app)


VALID_PAYLOAD = {
    "course_code": "CS101",
    "max_members": 4,
    "slots": [{"day": "Monday", "start_hour": 14, "end_hour": 16}],
}


def test_create_valid_group(client):
    r = client.post("/study-groups", json=VALID_PAYLOAD)
    assert r.status_code == 201
    assert r.json() == {"course_code": "CS101", "max_members": 4, "slot_count": 1}


def test_max_members_out_of_range_422(client):
    payload = {**VALID_PAYLOAD, "max_members": 20}
    r = client.post("/study-groups", json=payload)
    assert r.status_code == 422


def test_empty_slots_422(client):
    payload = {**VALID_PAYLOAD, "slots": []}
    r = client.post("/study-groups", json=payload)
    assert r.status_code == 422


def test_end_before_start_400(client):
    payload = {**VALID_PAYLOAD, "slots": [{"day": "Tuesday", "start_hour": 15, "end_hour": 10}]}
    r = client.post("/study-groups", json=payload)
    assert r.status_code == 400
    assert "Tuesday" in r.json()["detail"]
