# Depends injects shared work, Query adds query validation, and status names response codes.
from fastapi import Depends, FastAPI, HTTPException, Query, status
# Session performs database work; select builds a SQL query without writing SQL strings.
from sqlmodel import Session, select

# Import our database dependency/startup function and the three model shapes.
from app.database import get_session, init_db
from app.models import Listing, ListingCreate, ListingUpdate

# Create the app object and create the SQLite table before handling requests.
app = FastAPI(title="Campus Marketplace - Module 6")
init_db()


@app.get("/listings", response_model=list[Listing])
def list_listings(q: str | None = None, max_price_cents: int | None = Query(None, ge=0), session: Session = Depends(get_session)):
    # Start with the SQL equivalent of SELECT * FROM listing.
    statement = select(Listing)
    # Only add this WHERE condition when the optional title filter was supplied.
    if q:
        statement = statement.where(Listing.title.contains(q))
    # `is not None` allows 0 as a valid maximum price.
    if max_price_cents is not None:
        statement = statement.where(Listing.price_cents <= max_price_cents)
    # Execute the statement and convert the database result into a Python list.
    return session.exec(statement).all()


@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    # Session.get performs a primary-key lookup.
    listing = session.get(Listing, listing_id)
    # Return a standard API error when SQLite did not find a matching row.
    if listing is None:
        raise HTTPException(404, "Listing not found")
    return listing


@app.post("/listings", response_model=Listing, status_code=status.HTTP_201_CREATED)
def create_listing(listing_in: ListingCreate, session: Session = Depends(get_session)):
    # Convert the validated request model into a database table model.
    listing = Listing(**listing_in.model_dump())
    # Stage the new row, write it permanently, then reload its generated id.
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@app.put("/listings/{listing_id}", response_model=Listing)
def update_listing(listing_id: int, listing_in: ListingUpdate, session: Session = Depends(get_session)):
    # First retrieve the row that the URL identifies.
    listing = session.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Listing not found")
    # exclude_unset prevents missing fields from overwriting existing values with None.
    for name, value in listing_in.model_dump(exclude_unset=True).items():
        # setattr changes the matching attribute dynamically, e.g. listing.price_cents.
        setattr(listing, name, value)
    # Save and refresh the edited row before returning it.
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@app.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(listing_id: int, session: Session = Depends(get_session)):
    # Look up the row first so a missing id still receives a useful 404.
    listing = session.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Listing not found")
    # Mark the row for deletion, then commit that deletion to SQLite.
    session.delete(listing)
    session.commit()


# Import after declaring routes so the adapter can read the complete OpenAPI schema.
from fastapi_mcp import FastApiMCP  # noqa: E402

# Wrap this FastAPI app; the adapter creates MCP tools from the existing routes.
mcp = FastApiMCP(app)
# Mount the MCP server at /mcp so a client such as Copilot can connect to it.
mcp.mount()
