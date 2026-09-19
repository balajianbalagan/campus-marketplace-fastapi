def _auth_headers(client, username="seller1"):
    client.post("/auth/register", json={
        "username": username, "email": f"{username}@campus.edu", "password": "pw12345"
    })
    r = client.post("/auth/login", data={"username": username, "password": "pw12345"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_listing(client):
    headers = _auth_headers(client)
    r = client.post("/listings", json={
        "title": "Used Calculus Textbook", "description": "Barely used", "price_cents": 1500
    }, headers=headers)
    assert r.status_code == 201
    listing_id = r.json()["id"]

    r = client.get(f"/listings/{listing_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Used Calculus Textbook"


def test_create_listing_requires_auth(client):
    r = client.post("/listings", json={"title": "No Auth Item", "price_cents": 100})
    assert r.status_code == 401


def test_get_missing_listing_404(client):
    r = client.get("/listings/999999")
    assert r.status_code == 404


def test_only_seller_can_update(client):
    headers1 = _auth_headers(client, "seller_a")
    headers2 = _auth_headers(client, "seller_b")

    r = client.post("/listings", json={"title": "Desk Lamp", "price_cents": 500}, headers=headers1)
    listing_id = r.json()["id"]

    r = client.patch(f"/listings/{listing_id}", json={"price_cents": 400}, headers=headers2)
    assert r.status_code == 403


def test_search_by_title_and_price(client):
    headers = _auth_headers(client, "seller_c")
    client.post("/listings", json={"title": "Bike Lock", "price_cents": 800}, headers=headers)
    client.post("/listings", json={"title": "Bike Helmet", "price_cents": 2000}, headers=headers)

    r = client.get("/listings", params={"q": "Bike", "max_price_cents": 1000})
    titles = [l["title"] for l in r.json()]
    assert titles == ["Bike Lock"]
