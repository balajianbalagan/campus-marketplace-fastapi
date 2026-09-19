"""
Campus Marketplace MCP server.

Wraps the Campus Marketplace FastAPI app (must already be running locally,
see ../campus-marketplace/README.md) as an MCP server so
that any MCP client -- VS Code Copilot Chat, Claude, etc. -- can search,
inspect, and create listings using natural language instead of calling the
REST API by hand.

This is a thin adapter: every tool below just makes an HTTP call to the
already-running FastAPI app on http://127.0.0.1:8000. The MCP server holds
no business logic of its own -- FastAPI still owns validation, auth, and
persistence.
"""

import httpx
from mcp.server.fastmcp import FastMCP

API_BASE_URL = "http://127.0.0.1:8000"

# One MCP server, named "campus-marketplace" -- this name is what shows up
# in VS Code's MCP tool list / Copilot Chat's tool picker.
mcp = FastMCP("campus-marketplace")

# Cached bearer token for the demo "session" -- set via the login tool below.
# A real integration would use a per-user token instead of one shared global.
_session_token: str | None = None


def _auth_headers() -> dict:
    if not _session_token:
        return {}
    return {"Authorization": f"Bearer {_session_token}"}


@mcp.tool()
async def login(username: str, password: str) -> str:
    """Log in to Campus Marketplace and remember the session token for later tool calls.

    Call this before create_listing if you haven't already logged in this session.
    """
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        resp = await client.post("/auth/login", data={"username": username, "password": password})
    if resp.status_code != 200:
        return f"Login failed ({resp.status_code}): {resp.text}"

    global _session_token
    _session_token = resp.json()["access_token"]
    return f"Logged in as {username}."


@mcp.tool()
async def search_listings(query: str = "", max_price_cents: int | None = None, limit: int = 20) -> str:
    """Search Campus Marketplace listings by title substring and/or maximum price.

    Args:
        query: substring to match against listing titles (case-sensitive, leave empty for "no filter").
        max_price_cents: only return listings at or below this price, in cents.
        limit: maximum number of results (default 20, max 100).
    """
    params = {"limit": limit}
    if query:
        params["q"] = query
    if max_price_cents is not None:
        params["max_price_cents"] = max_price_cents

    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        resp = await client.get("/listings", params=params)
    resp.raise_for_status()

    listings = resp.json()
    if not listings:
        return "No listings matched."
    lines = [f"#{l['id']} — {l['title']} — ${l['price_cents'] / 100:.2f}" for l in listings]
    return "\n".join(lines)


@mcp.tool()
async def get_listing(listing_id: int) -> str:
    """Get full detail for a single listing by its id."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        resp = await client.get(f"/listings/{listing_id}")
    if resp.status_code == 404:
        return f"No listing with id {listing_id}."
    resp.raise_for_status()
    return str(resp.json())


@mcp.tool()
async def create_listing(title: str, description: str, price_cents: int) -> str:
    """Create a new Campus Marketplace listing as the currently logged-in user.

    Requires calling login() first in this session.
    """
    if not _session_token:
        return "Not logged in -- call login(username, password) first."

    payload = {"title": title, "description": description, "price_cents": price_cents}
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        resp = await client.post("/listings", json=payload, headers=_auth_headers())

    if resp.status_code == 429:
        return "Rate limited -- too many listings created recently, try again in a minute."
    if resp.status_code != 201:
        return f"Failed to create listing ({resp.status_code}): {resp.text}"

    listing = resp.json()
    return f"Created listing #{listing['id']}: {listing['title']} (${listing['price_cents'] / 100:.2f})"


if __name__ == "__main__":
    # stdio transport: VS Code / Copilot launches this script as a subprocess
    # and talks MCP over stdin/stdout -- no network port of its own.
    mcp.run(transport="stdio")
