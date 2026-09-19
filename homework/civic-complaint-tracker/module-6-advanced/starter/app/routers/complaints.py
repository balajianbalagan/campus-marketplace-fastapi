from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.auth import get_current_user, require_role
from app.database import get_session
from app.models import Complaint, ComplaintCreate, ComplaintRead, ComplaintUpdate, Role, User
from app.rate_limit import complaint_rate_limit
from app.ws import manager

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.get("", response_model=list[ComplaintRead])
def list_complaints(
    category: str | None = None,
    status: str | None = None,
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Complaint)
    if category:
        statement = statement.where(Complaint.category == category)
    if status:
        statement = statement.where(Complaint.status == status)
    return session.exec(statement.limit(limit)).all()


@router.get("/{complaint_id}", response_model=ComplaintRead)
def get_complaint(complaint_id: int, session: Session = Depends(get_session)):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


# TODO(module-6): add `dependencies=[Depends(complaint_rate_limit)]` to this route once
# app/rate_limit.py's RateLimiter is implemented.
@router.post("", response_model=ComplaintRead, status_code=201)
def create_complaint(
    complaint_in: ComplaintCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    complaint = Complaint(**complaint_in.model_dump(), reporter_id=user.id)
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return complaint


@router.patch("/{complaint_id}", response_model=ComplaintRead)
async def update_complaint(
    complaint_id: int,
    patch: ComplaintUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    changing_status = "status" in patch.model_dump(exclude_unset=True)
    if changing_status and user.role not in (Role.staff, Role.admin):
        raise HTTPException(status_code=403, detail="Only staff can change status")
    if not changing_status and complaint.reporter_id != user.id:
        raise HTTPException(status_code=403, detail="Not your complaint")

    for field, value in patch.model_dump(exclude_unset=True).items():
        setattr(complaint, field, value)
    session.add(complaint)
    session.commit()
    session.refresh(complaint)

    # TODO(module-6): once app/ws.py's ConnectionManager.broadcast is implemented, notify
    # anyone connected to the /ws/complaints feed when status changes:
    if changing_status:
        pass  # TODO: await manager.broadcast("complaints", {"event": "status_changed", "id": complaint.id, "status": complaint.status})

    return complaint
