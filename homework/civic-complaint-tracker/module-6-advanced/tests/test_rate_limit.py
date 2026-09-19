def test_sixth_complaint_in_a_minute_is_rate_limited(client, resident_headers):
    payload = {"category": "pothole", "description": "Same pothole, reported again", "location": "1st Ave"}

    statuses = []
    for _ in range(6):
        r = client.post("/complaints", json=payload, headers=resident_headers)
        statuses.append(r.status_code)

    assert statuses[:5] == [201] * 5, f"expected first 5 to succeed, got {statuses}"
    assert statuses[5] == 429, f"6th request in the same minute should be rate limited, got {statuses}"


def test_websocket_endpoint_exists(client):
    # Doesn't test broadcast content (hard to do well with TestClient) -- just that the
    # route is wired up and accepts a connection instead of 404ing / erroring on connect.
    with client.websocket_connect("/ws/complaints") as ws:
        pass
