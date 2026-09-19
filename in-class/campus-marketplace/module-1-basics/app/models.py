from pydantic import BaseModel, Field


class ListingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    price_cents: int = Field(ge=0)
    seller_name: str = Field(min_length=2, max_length=50)


class Listing(ListingCreate):
    id: int
