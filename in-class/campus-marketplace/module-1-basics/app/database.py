from sqlmodel import SQLModel, Session, create_engine

# SQLite file lives next to this file; check_same_thread=False because
# Starlette can hand each request to a different thread, but the default
# sqlite3 driver refuses cross-thread use unless we tell it that's fine.
DATABASE_URL = "sqlite:///./campus_marketplace.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create tables from every SQLModel subclass with table=True. Safe to call every startup."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: one Session per request, closed automatically after the response."""
    with Session(engine) as session:
        yield session
