# SQLModel supplies table metadata and sessions; create_engine configures the database connection.
from sqlmodel import SQLModel, Session, create_engine

# This URL creates a SQLite file beside the project; the thread option is required by SQLite with FastAPI.
engine = create_engine("sqlite:///./campus_marketplace.db", connect_args={"check_same_thread": False})


def init_db():
    # Read every SQLModel table class and create any table that does not already exist.
    SQLModel.metadata.create_all(engine)


def get_session():
    # Open a session for one request; code after `yield` closes it automatically.
    with Session(engine) as session:
        # FastAPI injects this object into a route that declares Depends(get_session).
        yield session
