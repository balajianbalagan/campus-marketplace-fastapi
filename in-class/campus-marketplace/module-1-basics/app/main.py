from fastapi import FastAPI, HTTPException, status

from app.models import Listing, ListingCreate

app = FastAPI(title="Campus Marketplace - Module 1")
listings: list[Listing] = []
next_listing_id = 1


@app.get("/")
def root():
    return {"message": "Campus Marketplace - see /docs"}


@app.get("/listings", response_model=list[Listing])
def list_listings():
    return listings


@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int):
    for listing in listings:
        if listing.id == listing_id:
            return listing
    raise HTTPException(status_code=404, detail="Listing not found")


@app.post("/listings", response_model=Listing, status_code=status.HTTP_201_CREATED)
def create_listing(listing_in: ListingCreate):
    global next_listing_id
    listing = Listing(id=next_listing_id, **listing_in.model_dump())
    next_listing_id += 1
    listings.append(listing)
    return listing
