from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.errors import MarketplaceError, marketplace_error_handler
from app.routers import auth, listings
from app.ws import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # create SQLite tables before we accept any traffic
    yield
    # nothing to tear down for SQLite; a real DB pool would close here


app = FastAPI(title="Campus Marketplace", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # classroom demo only -- lock this down for a real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(MarketplaceError, marketplace_error_handler)

app.include_router(auth.router)
app.include_router(listings.router)

app.mount("/static", StaticFiles(directory="uploads"), name="static")


@app.get("/")
def root():
    return {"message": "Campus Marketplace API -- see /docs"}


@app.websocket("/ws/listings")
async def listings_feed(websocket: WebSocket):
    """Live feed: connect, then receive a JSON message every time someone posts a new listing."""
    await manager.connect("listings", websocket)
    try:
        while True:
            await websocket.receive_text()   # keep the connection open; we ignore whatever client sends
    except WebSocketDisconnect:
        manager.disconnect("listings", websocket)


# Same one-line MCP mount as module-1-basics -- fastapi-mcp works the same way
# regardless of how many routes/auth dependencies the app has (it skips the
# websocket route above automatically since MCP tools are request/response, not streaming).
from fastapi_mcp import FastApiMCP  # noqa: E402

mcp = FastApiMCP(app)
mcp.mount()
