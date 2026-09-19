def _create_complaint(client, headers):
    r = client.post("/complaints", json={
        "category": "streetlight", "description": "Streetlight out for a week", "location": "Elm St"
    }, headers=headers)
    assert r.status_code == 201
    return r.json()["id"]


def test_created_complaint_has_reporter_id(client, resident_headers):
    complaint_id = _create_complaint(client, resident_headers)
    r = client.get(f"/complaints/{complaint_id}")
    assert r.json()["reporter_id"] is not None


def test_resident_cannot_change_status(client, resident_headers):
    complaint_id = _create_complaint(client, resident_headers)
    r = client.patch(f"/complaints/{complaint_id}", json={"status": "resolved"}, headers=resident_headers)
    assert r.status_code == 403


def test_staff_can_change_status(client, resident_headers, staff_headers):
    complaint_id = _create_complaint(client, resident_headers)
    r = client.patch(f"/complaints/{complaint_id}", json={"status": "resolved"}, headers=staff_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "resolved"


def test_resident_can_edit_own_description(client, resident_headers):
    complaint_id = _create_complaint(client, resident_headers)
    r = client.patch(f"/complaints/{complaint_id}", json={"description": "Updated: even more dangerous now"}, headers=resident_headers)
    assert r.status_code == 200
