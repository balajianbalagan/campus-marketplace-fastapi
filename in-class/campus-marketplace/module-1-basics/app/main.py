# FastAPI builds the web application; HTTPException returns API errors; status names HTTP codes.
from fastapi import FastAPI, HTTPException, status

# Import the validated input shape and the full response shape from our own module.
from app.models import Listing, ListingCreate

# Create the application object that Uvicorn will serve as `app.main:app`.
app = FastAPI(title="Campus Marketplace - Module 1")
# This Python list is temporary storage for Module 1; it resets when the server restarts.
listings: list[Listing] = []
# This counter imitates the id a database will assign in Module 2.
next_listing_id = 1


@app.get("/")
def root():
    # A small health route confirms that FastAPI is running.
    return {"message": "Campus Marketplace - see /docs"}


@app.get("/listings", response_model=list[Listing])
def list_listings():
    # FastAPI converts every Listing model in the list into JSON.
    return listings


@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int):
    # `listing_id` comes from the URL and FastAPI converts it to an int.
    for listing in listings:
        # Check each stored listing until its id matches the requested id.
        if listing.id == listing_id:
            return listing
    # Raising this exception stops the function and sends a JSON 404 response.
    raise HTTPException(status_code=404, detail="Listing not found")


@app.post("/listings", response_model=Listing, status_code=status.HTTP_201_CREATED)
def create_listing(listing_in: ListingCreate):
    # We modify the module-level counter, so Python requires `global` here.
    global next_listing_id
    # model_dump turns validated input into a dictionary; ** passes its keys as named arguments.
    listing = Listing(id=next_listing_id, **listing_in.model_dump())
    # Reserve the next number before the next request creates another listing.
    next_listing_id += 1
    # Append the listing to the temporary in-memory collection.
    listings.append(listing)
    # FastAPI serializes the model and uses the declared 201 Created status code.
    return listing
