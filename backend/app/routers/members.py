from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/api/members", tags=["members"])


@router.post("", response_model=schemas.MemberOut, status_code=201)
def create_member(payload: schemas.MemberCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Member).filter(models.Member.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="A member with this email already exists")

    member = models.Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.get("", response_model=List[schemas.MemberOut])
def list_members(q: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Member)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Member.name.ilike(like)) | (models.Member.email.ilike(like))
        )
    return query.order_by(models.Member.name).all()


@router.get("/{member_id}", response_model=schemas.MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/{member_id}", response_model=schemas.MemberOut)
def update_member(member_id: int, payload: schemas.MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)
    return member