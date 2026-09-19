# BaseModel turns this class into a validated JSON request/response shape.
from pydantic import BaseModel, Field


class ListingCreate(BaseModel):
    """The fields a client may send when it creates a listing."""

    # `str` tells FastAPI to require text; Field adds validation limits.
    title: str = Field(min_length=3, max_length=100)
    # Prices are stored as integer paise, so there is no floating-point rounding issue.
    price_cents: int = Field(ge=0)
    # The seller name is also required and kept to a sensible length.
    seller_name: str = Field(min_length=2, max_length=50)


class Listing(ListingCreate):
    """The complete listing returned by the API after the server assigns an id."""

    # Clients do not choose this value; the server adds it when saving the listing.
    id: int
