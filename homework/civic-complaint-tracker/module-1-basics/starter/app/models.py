from datetime import datetime

from sqlmodel import Field, SQLModel

# Given: the shared fields. You should NOT need to touch this class.
class ComplaintBase(SQLModel):
    category: str
    description: str = Field(min_length=10)
    location: str
    reporter_name: str


# TODO(module-1): finish the table model.
# It needs: id (primary key, optional int defaulting to None), status (str, default "open"),
# and created_at (datetime, default_factory=datetime.utcnow).
# Look at Campus Marketplace's `Listing(ListingBase, table=True)` for the exact shape.
class Complaint(ComplaintBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # TODO: add status and created_at fields here
    ...


# TODO(module-1): this is what a client sends to create a complaint.
# It should NOT include id, status, or created_at (the server controls all three).
class ComplaintCreate(ComplaintBase):
    ...


# TODO(module-1): this is what the server sends back.
# It SHOULD include id, status, and created_at, on top of the base fields.
class ComplaintRead(ComplaintBase):
    ...


# Given: partial update payload for PATCH /complaints/{id}.
class ComplaintUpdate(SQLModel):
    status: str | None = None
