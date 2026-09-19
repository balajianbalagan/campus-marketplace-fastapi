import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

# Point the app at a throwaway test DB before importing it, so we never touch campus_marketplace.db
os.environ.setdefault("CAMPUS_MARKETPLACE_TEST", "1")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    from app import database

    test_db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_URL", f"sqlite:///{test_db_path}")

    from sqlmodel import create_engine

    test_engine = create_engine(f"sqlite:///{test_db_path}", connect_args={"check_same_thread": False})
    monkeypatch.setattr(database, "engine", test_engine)
    SQLModel.metadata.create_all(test_engine)

    from app.main import app

    with TestClient(app) as c:
        yield c
