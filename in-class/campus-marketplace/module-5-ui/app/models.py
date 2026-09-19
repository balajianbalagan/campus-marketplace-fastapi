# SQLModel combines Pydantic validation with SQLAlchemy database mapping.
from sqlmodel import Field, SQLModel


class ListingBase(SQLModel):
    """Fields shared by stored listings and create requests."""

    # Field constraints become both runtime validation and Swagger documentation.
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    price_cents: int = Field(ge=0)
    seller_name: str = Field(min_length=2, max_length=50)


class Listing(ListingBase, table=True):
    """`table=True` tells SQLModel to create a SQLite table for this class."""

    # None before insertion lets SQLite generate the primary-key value.
    id: int | None = Field(default=None, primary_key=True)


class ListingCreate(ListingBase):
    """Input for POST; it deliberately has no client-supplied id."""
    pass


class ListingUpdate(SQLModel):
    """All fields are optional so PUT can change only supplied values."""
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price_cents: int | None = Field(default=None, ge=0)
    seller_name: str | None = Field(default=None, min_length=2, max_length=50)
