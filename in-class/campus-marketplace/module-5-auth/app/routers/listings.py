import shutil
import uuid
from pathlib import Path as FSPath

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from app.auth import get_current_user, require_role
from app.database import get_session
from app.models import Listing, ListingCreate, ListingRead, ListingUpdate, Role, User

router = APIRouter(prefix="/listings", tags=["listings"])

UPLOAD_DIR = FSPath("uploads/listings")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("", response_model=list[ListingRead])
def search_listings(
    q: str | None = Query(None, min_length=1, max_length=50, description="title contains..."),
    max_price_cents: int | None = None,
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Listing)
    if q:
        statement = statement.where(Listing.title.contains(q))
    if max_price_cents is not None:
        statement = statement.where(Listing.price_cents <= max_price_cents)
    statement = statement.limit(limit)
    return session.exec(statement).all()


@router.get("/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: int, session: Session = Depends(get_session)):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("", response_model=ListingRead, status_code=201)
def create_listing(
    listing_in: ListingCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    listing = Listing(**listing_in.model_dump(), seller_id=user.id)
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@router.patch("/{listing_id}", response_model=ListingRead)
def update_listing(
    listing_id: int,
    patch: ListingUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not your listing")

    # exclude_unset: only overwrite fields the client actually sent, not every field's default
    for field, value in patch.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)

    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing


@router.delete("/{listing_id}", status_code=204)
def delete_listing(
    listing_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(require_role(Role.moderator, Role.admin)),
):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    session.delete(listing)
    session.commit()


@router.post("/{listing_id}/photo", response_model=ListingRead)
async def upload_photo(
    listing_id: int,
    photo: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not your listing")
    if photo.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG allowed")

    # Never trust the client's filename on disk -- generate our own to avoid path traversal.
    ext = photo.filename.rsplit(".", 1)[-1] if "." in photo.filename else "bin"
    dest = UPLOAD_DIR / f"{uuid.uuid4()}.{ext}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    listing.photo_url = f"/static/listings/{dest.name}"
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing
