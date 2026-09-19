from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.database import init_db
from app.routers import auth, complaints
from app.ws import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Civic Complaint Tracker", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(complaints.router)


@app.get("/")
def root():
    return {"message": "Civic Complaint Tracker API -- see /docs"}


# TODO(module-6): connect to the "complaints" room via manager.connect, then loop
# `await websocket.receive_text()` to keep the connection open, catching WebSocketDisconnect
# to call manager.disconnect. See Campus Marketplace's /ws/listings route for the pattern.
@app.websocket("/ws/complaints")
async def complaints_feed(websocket: WebSocket):
    raise NotImplementedError("TODO: implement complaints_feed")
