# Module 6 — Advanced FastAPI Patterns (knowledge base)

10 lessons. This is where Campus Marketplace gets the features that make the MCP/Copilot demo feel alive.

## 1–2. Async endpoints, concurrency, async dependencies & lifespan

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up: warm caches, open connection pools")
    yield
    print("shutting down: close connection pools")

app = FastAPI(lifespan=lifespan)

@app.get("/listings/{id}")
async def get_listing(id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Listing).where(Listing.id == id))
    return result.first()
```

`async def` only helps when everything you `await` inside is also async (async DB driver, `httpx.AsyncClient`, not blocking `requests`/sync SQLAlchemy) — mixing a blocking call into an `async def` route blocks the whole event loop, not just that request. `lifespan` replaces the old `@app.on_event("startup"/"shutdown")` — one context manager, setup before `yield`, teardown after.

## 3–4. WebSockets — basics, rooms & broadcasting

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room, []).append(ws)

    def disconnect(self, room: str, ws: WebSocket):
        self.rooms[room].remove(ws)

    async def broadcast(self, room: str, message: dict):
        for ws in self.rooms.get(room, []):
            await ws.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/listings")
async def listings_feed(websocket: WebSocket):
    await manager.connect("listings", websocket)
    try:
        while True:
            await websocket.receive_text()   # keep connection open; ignore client pings
    except WebSocketDisconnect:
        manager.disconnect("listings", websocket)
```

Used for "new listing posted" live notifications — call `await manager.broadcast("listings", {...})` inside `create_listing` after saving. `receive_text()` in a loop is what keeps the coroutine (and the connection) alive; the `try/except WebSocketDisconnect` is required cleanup or the room list leaks dead sockets.

## 5. Custom middleware & request processing

```python
import time, logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logging.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)")
    return response
```

Runs for *every* request before routing. Good for cross-cutting concerns (logging, timing, request IDs) — bad place for per-route business logic (use a dependency for that instead, so it's visible in `/docs`).

## 6. Rate limiting with dependencies

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times, self.seconds = times, seconds
        self.hits: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request: Request):
        key = request.client.host
        now = time.time()
        self.hits[key] = [t for t in self.hits[key] if now - t < self.seconds]
        if len(self.hits[key]) >= self.times:
            raise HTTPException(429, "Too many requests")
        self.hits[key].append(now)

listing_rate_limit = RateLimiter(times=5, seconds=60)

@app.post("/listings", dependencies=[Depends(listing_rate_limit)])
def create_listing(...): ...
```

Rate limiting as a **class-based dependency** (Module 1's "Classes as Dependencies") — the class holds config + state, `__call__` makes it usable via `Depends(...)`. In-memory like this resets on restart and doesn't share state across multiple server processes — for production, back it with Redis instead of a dict.

## 7. Response caching patterns

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def get_categories() -> list[str]:
    return session.exec(select(Category.name)).all()   # rarely changes, expensive-ish query
```

`lru_cache` is fine for small, rarely-changing, process-local data (categories, config). For per-request data that changes often (listing search results), you want a TTL cache (`cachetools.TTLCache`) or Redis with an explicit invalidation on write — don't cache anything a user expects to see update immediately after their own action.

## 8. Custom response types

```python
from fastapi.responses import StreamingResponse, ORJSONResponse

@app.get("/listings/export", response_class=StreamingResponse)
def export_csv():
    def rows():
        yield "id,title,price_cents\n"
        for l in db.all_listings():
            yield f"{l.id},{l.title},{l.price_cents}\n"
    return StreamingResponse(rows(), media_type="text/csv")

app = FastAPI(default_response_class=ORJSONResponse)  # faster JSON serialization app-wide
```

Use `StreamingResponse` when the payload is large or generated incrementally (CSV export, log tail) so you don't buffer the whole thing in memory first.

## 9. Application events & startup logic

Covered by `lifespan` above — this lesson is the "why": seed default categories, create the SQLite file/tables, open a connection pool, warm an in-memory cache — all before the app starts accepting traffic, and cleaned up on shutdown so nothing leaks between test runs or redeploys.

## 10. API versioning & router composition

```python
# app/routers/v1/listings.py
router_v1 = APIRouter(prefix="/v1/listings", tags=["listings-v1"])

# app/routers/v2/listings.py
router_v2 = APIRouter(prefix="/v2/listings", tags=["listings-v2"])  # e.g. adds pagination cursor instead of offset

app.include_router(router_v1)
app.include_router(router_v2)
```

Version at the router level, not with `if` branches inside one handler — old clients keep hitting `/v1/...` unchanged while you iterate on `/v2/...`. `APIRouter(prefix=..., tags=...)` composition (from Module 1's "Bigger Applications") is the whole mechanism; versioning is just "use it twice with different prefixes."
