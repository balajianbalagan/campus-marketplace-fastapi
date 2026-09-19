from sqlmodel import Field, SQLModel


class ListingBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    price_cents: int = Field(ge=0)
    seller_name: str = Field(min_length=2, max_length=50)


class Listing(ListingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ListingCreate(ListingBase):
    pass


class ListingUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price_cents: int | None = Field(default=None, ge=0)
    seller_name: str | None = Field(default=None, min_length=2, max_length=50)
