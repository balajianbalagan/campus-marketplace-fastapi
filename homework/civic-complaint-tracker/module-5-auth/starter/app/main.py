from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import auth, complaints


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Civic Complaint Tracker", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(complaints.router)

app.mount("/static", StaticFiles(directory="uploads"), name="static")


@app.get("/")
def root():
    return {"message": "Civic Complaint Tracker API -- see /docs"}
