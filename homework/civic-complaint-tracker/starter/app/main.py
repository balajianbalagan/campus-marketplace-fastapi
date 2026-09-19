from fastapi import Depends, FastAPI
from sqlmodel import Session

from app.database import get_session, init_db
from app.models import Complaint, ComplaintCreate, ComplaintUpdate

app = FastAPI(title="Civic Complaint Tracker")
init_db()


@app.get("/complaints", response_model=list[Complaint])
def list_complaints(
    category: str | None = None,
    status: str | None = None,
    session: Session = Depends(get_session),
):
    # TODO: build a select(Complaint) statement and apply the optional filters.
    raise NotImplementedError("Implement list_complaints")


@app.get("/complaints/{complaint_id}", response_model=Complaint)
def get_complaint(complaint_id: int, session: Session = Depends(get_session)):
    # TODO: return the complaint or raise HTTPException(404, ...).
    raise NotImplementedError("Implement get_complaint")


@app.post("/complaints", response_model=Complaint, status_code=201)
def create_complaint(complaint_in: ComplaintCreate, session: Session = Depends(get_session)):
    # TODO: create, commit, refresh, and return a Complaint.
    raise NotImplementedError("Implement create_complaint")


@app.put("/complaints/{complaint_id}", response_model=Complaint)
def update_complaint(
    complaint_id: int,
    complaint_in: ComplaintUpdate,
    session: Session = Depends(get_session),
):
    # TODO: update only fields that the client supplied.
    raise NotImplementedError("Implement update_complaint")


@app.delete("/complaints/{complaint_id}", status_code=204)
def delete_complaint(complaint_id: int, session: Session = Depends(get_session)):
    # TODO: delete the complaint or raise HTTPException(404, ...).
    raise NotImplementedError("Implement delete_complaint")


# TODO Module 6: mount FastApiMCP(app) here after your CRUD routes work.
