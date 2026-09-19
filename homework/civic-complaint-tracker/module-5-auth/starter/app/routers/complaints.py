import shutil
import uuid
from pathlib import Path as FSPath

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from app.auth import get_current_user, require_role
from app.database import get_session
from app.models import Complaint, ComplaintCreate, ComplaintRead, ComplaintUpdate, Role, User

router = APIRouter(prefix="/complaints", tags=["complaints"])

UPLOAD_DIR = FSPath("uploads/complaints")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# given: unchanged from Module 1, other than requiring login to view the list.
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


# TODO(module-5): set reporter_id = user.id (from Depends(get_current_user)) instead of
# leaving it out -- Complaint.reporter_id is a required field now.
@router.post("", response_model=ComplaintRead, status_code=201)
def create_complaint(
    complaint_in: ComplaintCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    complaint = Complaint(**complaint_in.model_dump())  # TODO: pass reporter_id=user.id too
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return complaint


# TODO(module-5): only staff/admin may change `status`. Residents may still edit their OWN
# complaint's description/location. Use require_role for the status check, and compare
# complaint.reporter_id to the current user for the description/location check (403 if
# neither condition is met for the fields being changed).
@router.patch("/{complaint_id}", response_model=ComplaintRead)
def update_complaint(
    complaint_id: int,
    patch: ComplaintUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    raise NotImplementedError("TODO: implement the role/ownership checks, then apply patch")


# TODO(module-5): only the original reporter may upload a photo for their own complaint.
# Validate content_type is image/jpeg or image/png (400 otherwise). Generate the on-disk
# filename with uuid4() -- never trust photo.filename. Save under UPLOAD_DIR, set
# complaint.photo_url, commit, return the updated complaint.
@router.post("/{complaint_id}/photo", response_model=ComplaintRead)
async def upload_photo(
    complaint_id: int,
    photo: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    raise NotImplementedError("TODO: implement upload_photo")
