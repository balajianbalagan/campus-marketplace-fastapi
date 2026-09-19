from sqlmodel import SQLModel, Session, create_engine

# This part is given -- identical pattern to Campus Marketplace's app/database.py.
DATABASE_URL = "sqlite:///./complaints.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
