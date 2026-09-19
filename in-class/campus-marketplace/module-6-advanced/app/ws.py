from fastapi import WebSocket


class ConnectionManager:
    """Tracks open websocket connections per 'room' so we can broadcast to all of them."""

    def __init__(self) -> None:
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.rooms.setdefault(room, []).append(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if websocket in self.rooms.get(room, []):
            self.rooms[room].remove(websocket)

    async def broadcast(self, room: str, message: dict) -> None:
        for websocket in list(self.rooms.get(room, [])):
            await websocket.send_json(message)


manager = ConnectionManager()
