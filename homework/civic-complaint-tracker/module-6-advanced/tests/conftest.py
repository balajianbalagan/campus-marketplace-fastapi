import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine


@pytest.fixture()
def client(tmp_path, monkeypatch):
    from app import database

    test_db_path = tmp_path / "test.db"
    test_engine = create_engine(f"sqlite:///{test_db_path}", connect_args={"check_same_thread": False})
    monkeypatch.setattr(database, "engine", test_engine)
    SQLModel.metadata.create_all(test_engine)

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    # complaint_rate_limit is a module-level singleton; without this, hits from one test
    # would carry into the next since TestClient's host is always "testclient".
    from app.rate_limit import complaint_rate_limit
    complaint_rate_limit.hits.clear()
    yield
    complaint_rate_limit.hits.clear()


@pytest.fixture()
def resident_headers(client):
    client.post("/auth/register", json={
        "username": "resident1", "email": "resident1@city.gov", "password": "pw12345"
    })
    r = client.post("/auth/login", data={"username": "resident1", "password": "pw12345"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
