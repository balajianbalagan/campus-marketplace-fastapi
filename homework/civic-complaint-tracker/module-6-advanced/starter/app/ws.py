from fastapi import WebSocket


class ConnectionManager:
    """Tracks open websocket connections per 'room' so we can broadcast to all of them.

    See in-class/campus-marketplace/module-6-advanced/app/ws.py for the reference implementation -- same shape here.
    """

    def __init__(self) -> None:
        self.rooms: dict[str, list[WebSocket]] = {}

    # TODO(module-6): accept the websocket connection, then add it to self.rooms[room]
    # (use setdefault to create the list if the room doesn't exist yet).
    async def connect(self, room: str, websocket: WebSocket) -> None:
        raise NotImplementedError("TODO: implement connect")

    # TODO(module-6): remove websocket from self.rooms[room] if it's there.
    def disconnect(self, room: str, websocket: WebSocket) -> None:
        raise NotImplementedError("TODO: implement disconnect")

    # TODO(module-6): send `message` (a dict) as JSON to every websocket in self.rooms[room].
    async def broadcast(self, room: str, message: dict) -> None:
        raise NotImplementedError("TODO: implement broadcast")


manager = ConnectionManager()
