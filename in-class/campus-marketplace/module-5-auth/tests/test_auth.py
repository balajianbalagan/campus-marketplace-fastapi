def test_register_and_login(client):
    r = client.post("/auth/register", json={
        "username": "alice", "email": "alice@campus.edu", "password": "s3cret!"
    })
    assert r.status_code == 201
    assert r.json()["username"] == "alice"
    assert "hashed_password" not in r.json()   # response_model strips it

    r = client.post("/auth/login", data={"username": "alice", "password": "s3cret!"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "bob", "email": "bob@campus.edu", "password": "correct-horse"
    })
    r = client.post("/auth/login", data={"username": "bob", "password": "wrong"})
    assert r.status_code == 401


def test_duplicate_username_rejected(client):
    payload = {"username": "carol", "email": "carol@campus.edu", "password": "pw12345"}
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 400
