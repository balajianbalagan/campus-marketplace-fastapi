def test_register_and_login(client):
    r = client.post("/auth/register", json={
        "username": "dana", "email": "dana@city.gov", "password": "s3cret!"
    })
    assert r.status_code == 201
    assert "hashed_password" not in r.json()

    r = client.post("/auth/login", data={"username": "dana", "password": "s3cret!"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password_401(client):
    client.post("/auth/register", json={"username": "eve", "email": "eve@city.gov", "password": "correct"})
    r = client.post("/auth/login", data={"username": "eve", "password": "wrong"})
    assert r.status_code == 401


def test_create_complaint_requires_auth(client):
    r = client.post("/complaints", json={"category": "pothole", "description": "Deep pothole on Main St", "location": "Main St & 5th"})
    assert r.status_code == 401
