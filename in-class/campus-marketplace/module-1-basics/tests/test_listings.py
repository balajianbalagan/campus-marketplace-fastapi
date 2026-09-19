def test_create_and_list_listing(client):
    r = client.post("/listings", json={
        "title": "Used Calculus Textbook", "price_cents": 1500, "seller_name": "Priya"
    })
    assert r.status_code == 200
    listing_id = r.json()["id"]

    r = client.get("/listings")
    titles = [l["title"] for l in r.json()]
    assert "Used Calculus Textbook" in titles

    r = client.get(f"/listings/{listing_id}")
    assert r.status_code == 200
    assert r.json()["seller_name"] == "Priya"


def test_get_missing_listing_404(client):
    r = client.get("/listings/999999")
    assert r.status_code == 404


def test_empty_marketplace(client):
    r = client.get("/listings")
    assert r.status_code == 200
    assert r.json() == []
