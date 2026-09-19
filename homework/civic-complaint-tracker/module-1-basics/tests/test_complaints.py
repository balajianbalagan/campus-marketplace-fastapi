def test_create_complaint(client):
    r = client.post("/complaints", json={
        "category": "pothole",
        "description": "Deep pothole on Main St",
        "location": "Main St & 5th",
        "reporter_name": "Jordan",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "open"
    assert body["category"] == "pothole"


def test_create_complaint_forces_status_open(client):
    r = client.post("/complaints", json={
        "category": "trash", "description": "Overflowing bins on 3rd", "location": "3rd Ave",
        "reporter_name": "Alex", "status": "resolved",
    })
    assert r.json()["status"] == "open"


def test_get_missing_complaint_404(client):
    r = client.get("/complaints/999999")
    assert r.status_code == 404


def test_get_complaint(client):
    r = client.post("/complaints", json={
        "category": "graffiti", "description": "Graffiti on the library wall", "location": "Library",
        "reporter_name": "Sam",
    })
    complaint_id = r.json()["id"]

    r = client.get(f"/complaints/{complaint_id}")
    assert r.status_code == 200
    assert r.json()["location"] == "Library"


def test_list_filters_by_category(client):
    client.post("/complaints", json={
        "category": "streetlight", "description": "Streetlight out on Oak St", "location": "Oak St",
        "reporter_name": "Robin",
    })
    client.post("/complaints", json={
        "category": "pothole", "description": "Another pothole appeared here", "location": "Pine St",
        "reporter_name": "Robin",
    })

    r = client.get("/complaints", params={"category": "streetlight"})
    categories = {c["category"] for c in r.json()}
    assert categories == {"streetlight"}
