# Module 6 — Live updates & rate limiting

Starting point has full working auth + complaint CRUD (the Module 5 solution, given). This
module adds what Module 6 taught: a websocket feed for live status changes, and rate
limiting on complaint creation.

## What you need to build

### 1. `app/ws.py` — `ConnectionManager`

- `connect(room, websocket)` — accept the websocket, add it to `self.rooms[room]`.
- `disconnect(room, websocket)` — remove it from that room's list.
- `broadcast(room, message)` — send `message` (a dict, use `send_json`) to every websocket
  currently in that room.

### 2. `app/main.py` — `GET /ws/complaints`

A websocket route. `await manager.connect("complaints", websocket)`, then loop
`await websocket.receive_text()` forever to keep the connection alive, catching
`WebSocketDisconnect` to clean up via `manager.disconnect`.

### 3. Wire broadcasting into status changes

In `app/routers/complaints.py`'s `update_complaint`, after a `status` change is saved,
`await manager.broadcast("complaints", {"event": "status_changed", "id": ..., "status": ...})`.

### 4. `app/rate_limit.py` — `RateLimiter`

Same class-based-dependency shape as Campus Marketplace: `__init__(self, times, seconds)`
holds config + a `dict[str, list[float]]` of hit timestamps per client IP; `__call__` prunes
timestamps older than `seconds`, raises `HTTPException(429, ...)` if there are already
`times` or more hits in the window, otherwise records this hit.

Wire it into `POST /complaints` via `dependencies=[Depends(complaint_rate_limit)]`.

## Manual test for the websocket (no automated test for this one — sockets are hard to unit test well)

1. `uvicorn app.main:app --reload`
2. In a browser console on any page: 
   ```js
   const ws = new WebSocket("ws://127.0.0.1:8000/ws/complaints");
   ws.onmessage = (e) => console.log("got:", e.data);
   ```
3. In another terminal, log in, create a complaint, then `PATCH` its status via `/docs`.
4. Watch the browser console log the broadcast.

Run `python -m pytest ../tests -v` from `starter/` for the rate-limiting tests.
