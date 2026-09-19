from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Complaint

app = FastAPI(title="Civic Complaint Tracker")
init_db()


@app.get("/")
def root():
    return {"message": "Civic Complaint Tracker API -- see /docs"}


# TODO(module-1): GET /complaints
# - optional query param: category (str | None) -- if given, only return complaints with
#   that category
# - return session.exec(select(Complaint)...).all()
@app.get("/complaints")
def list_complaints(category: str | None = None, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement list_complaints")


# TODO(module-1): GET /complaints/{complaint_id}
# - session.get(Complaint, complaint_id)
# - 404 with HTTPException if not found
@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: int, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement get_complaint")


# TODO(module-1): POST /complaints
# - accept a Complaint body
# - force complaint.status = "open" and complaint.id = None (ignore anything the client sent
#   for those two fields -- the server decides them, not the caller)
# - session.add(complaint); session.commit(); session.refresh(complaint); return complaint
@app.post("/complaints")
def create_complaint(complaint: Complaint, session: Session = Depends(get_session)):
    raise NotImplementedError("TODO: implement create_complaint")
