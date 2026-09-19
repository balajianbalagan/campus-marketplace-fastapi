from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Listing

app = FastAPI(title="Campus Marketplace")
init_db()  # make sure the campus_marketplace.db file + table exist before we get any requests


@app.get("/")
def root():
    return {"message": "Campus Marketplace API -- see /docs"}


# GET /listings -- show everything for sale
@app.get("/listings")
def list_listings(session: Session = Depends(get_session)):
    return session.exec(select(Listing)).all()


# GET /listings/{id} -- show one item
@app.get("/listings/{listing_id}")
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


# POST /listings -- add a new item for sale
@app.post("/listings")
def create_listing(listing: Listing, session: Session = Depends(get_session)):
    session.add(listing)
    session.commit()
    session.refresh(listing)  # pulls back the id SQLite just assigned
    return listing


# --- Turn this API into an MCP server, so VS Code Copilot Chat can call it as tools. ---
# No extra code needed per endpoint -- fastapi-mcp reads the routes above and builds the
# tools automatically. See ../README.md for how to connect this to VS Code.
from fastapi_mcp import FastApiMCP  # noqa: E402  (imported down here so the app is fully defined first)

mcp = FastApiMCP(app)
mcp.mount()
