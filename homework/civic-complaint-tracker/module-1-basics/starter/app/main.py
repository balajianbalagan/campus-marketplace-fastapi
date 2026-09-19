from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Complaint, ComplaintCreate, ComplaintRead, ComplaintUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Civic Complaint Tracker", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Civic Complaint Tracker API -- see /docs"}


# TODO(module-1): POST /complaints
# - accept a ComplaintCreate body
# - build a Complaint from it (status should always be "open" here, ignore anything
#   the client might try to send for status -- ComplaintCreate shouldn't even have that field)
# - save it via the session, return the created row
# - response_model=ComplaintRead, status_code=201
@app.post("/complaints")
def create_complaint(complaint_in: ComplaintCreate, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement create_complaint")


# TODO(module-1): GET /complaints
# - optional query params: category (str | None), status (str | None), limit (int, default 20, le=100)
# - filter the SQL select() by whichever of category/status were provided
# - response_model=list[ComplaintRead]
@app.get("/complaints")
def list_complaints(
    category: str | None = None,
    status: str | None = None,
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    raise NotImplementedError("TODO: implement list_complaints")


# TODO(module-1): GET /complaints/{complaint_id}
# - 404 with HTTPException if not found
# - response_model=ComplaintRead
@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: int, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement get_complaint")


# TODO(module-1): PATCH /complaints/{complaint_id}
# - accept a ComplaintUpdate body
# - 404 if not found
# - use patch.model_dump(exclude_unset=True) so you only touch fields the client actually sent
# - response_model=ComplaintRead
@app.patch("/complaints/{complaint_id}")
def update_complaint(
    complaint_id: int,
    patch: ComplaintUpdate,
    session: Session = Depends(get_session),
):
    raise NotImplementedError("TODO: implement update_complaint")
