from sqlmodel import Field, SQLModel


# A "listing" is one item for sale. This one class is our whole data model for Module 1.
class Listing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    price_cents: int
    seller_name: str
