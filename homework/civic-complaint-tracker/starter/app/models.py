from sqlmodel import Field, SQLModel


class ComplaintBase(SQLModel):
    category: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=5, max_length=500)
    location: str = Field(min_length=3, max_length=100)
    reporter_name: str = Field(min_length=2, max_length=50)
    status: str = Field(default="open", pattern="^(open|in_progress|resolved)$")


class Complaint(ComplaintBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(SQLModel):
    description: str | None = Field(default=None, min_length=5, max_length=500)
    location: str | None = Field(default=None, min_length=3, max_length=100)
    status: str | None = Field(default=None, pattern="^(open|in_progress|resolved)$")
