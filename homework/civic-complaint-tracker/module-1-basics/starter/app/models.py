from sqlmodel import Field, SQLModel


# TODO(module-1): finish this model. It needs, on top of what's here:
# - description: str
# - location: str
# - reporter_name: str
# - status: str, defaulting to "open" (look at how `id` uses Field(default=...) below)
class Complaint(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category: str
    ...
