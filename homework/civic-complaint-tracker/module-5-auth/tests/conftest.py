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


@pytest.fixture()
def resident_headers(client):
    client.post("/auth/register", json={
        "username": "resident1", "email": "resident1@city.gov", "password": "pw12345"
    })
    r = client.post("/auth/login", data={"username": "resident1", "password": "pw12345"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def staff_headers(client):
    from sqlmodel import Session, select
    from app import database
    from app.models import Role, User

    client.post("/auth/register", json={
        "username": "staffer1", "email": "staffer1@city.gov", "password": "pw12345"
    })
    # No public "promote to staff" endpoint (rightly so) -- flip it directly in the test DB.
    with Session(database.engine) as session:
        user = session.exec(select(User).where(User.username == "staffer1")).first()
        user.role = Role.staff
        session.add(user)
        session.commit()

    r = client.post("/auth/login", data={"username": "staffer1", "password": "pw12345"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
