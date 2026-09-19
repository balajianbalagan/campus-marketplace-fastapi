import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import alert_rate_limiter, app
    alert_rate_limiter.hits.clear()
    return TestClient(app)


def test_websocket_connects(client):
    with client.websocket_connect("/ws/alerts") as ws:
        pass


def test_post_alert_succeeds(client):
    r = client.post("/alerts", json={"message": "Fire drill at 2pm"})
    assert r.status_code == 201
    assert r.json() == {"sent": True}


def test_fourth_alert_in_a_minute_rate_limited(client):
    statuses = []
    for _ in range(4):
        r = client.post("/alerts", json={"message": "test"})
        statuses.append(r.status_code)
    assert statuses[:3] == [201, 201, 201]
    assert statuses[3] == 429
