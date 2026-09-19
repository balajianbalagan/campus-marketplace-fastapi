import time
from collections import defaultdict

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI()


class AlertIn(BaseModel):
    message: str


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    # TODO: await websocket.accept(), then append it to self.connections
    async def connect(self, websocket: WebSocket):
        raise NotImplementedError

    # TODO: remove websocket from self.connections if present
    def disconnect(self, websocket: WebSocket):
        raise NotImplementedError

    # TODO: for each connection, await connection.send_json(message)
    async def broadcast(self, message: dict):
        raise NotImplementedError


manager = ConnectionManager()


# TODO: manager.connect(websocket), then `while True: await websocket.receive_text()`
# inside a try/except WebSocketDisconnect that calls manager.disconnect(websocket).
@app.websocket("/ws/alerts")
async def alerts_feed(websocket: WebSocket):
    raise NotImplementedError


class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds
        self.hits: dict[str, list[float]] = defaultdict(list)

    # TODO: key by request.client.host, prune hits older than self.seconds, 429 if
    # len(window) >= self.times, otherwise record this hit.
    def __call__(self, request: Request):
        raise NotImplementedError


alert_rate_limiter = RateLimiter(times=3, seconds=60)


# TODO: dependencies=[Depends(alert_rate_limiter)]; await manager.broadcast({"alert": alert.message});
# return {"sent": True}, status_code=201
@app.post("/alerts")
async def create_alert(alert: AlertIn):
    raise NotImplementedError
