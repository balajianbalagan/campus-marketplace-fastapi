from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Listing, ListingCreate, ListingUpdate

app = FastAPI(title="Campus Marketplace - Module 6")
init_db()


@app.get("/listings", response_model=list[Listing])
def list_listings(q: str | None = None, max_price_cents: int | None = Query(None, ge=0), session: Session = Depends(get_session)):
    statement = select(Listing)
    if q:
        statement = statement.where(Listing.title.contains(q))
    if max_price_cents is not None:
        statement = statement.where(Listing.price_cents <= max_price_cents)
    return session.exec(statement).all()


@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Listing not found")
    return listing


@app.post("/listings", response_model=Listing, status_code=status.HTTP_201_CREATED)
def create_listing(listing_in: ListingCreate, session: Session = Depends(get_session)):
    listing = Listing(**listing_in.model_dump())
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@app.put("/listings/{listing_id}", response_model=Listing)
def update_listing(listing_id: int, listing_in: ListingUpdate, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Listing not found")
    for name, value in listing_in.model_dump(exclude_unset=True).items():
        setattr(listing, name, value)
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@app.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(listing_id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(404, "Listing not found")
    session.delete(listing)
    session.commit()


from fastapi_mcp import FastApiMCP  # noqa: E402

mcp = FastApiMCP(app)
mcp.mount()
