from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/api/loans", tags=["loans"])


@router.post("", response_model=schemas.LoanOut, status_code=201)
def borrow_book(payload: schemas.LoanCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == payload.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    member = db.query(models.Member).filter(models.Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=409, detail="No copies of this book are currently available")

    already_out = (
        db.query(models.Loan)
        .filter(
            models.Loan.book_id == payload.book_id,
            models.Loan.member_id == payload.member_id,
            models.Loan.returned_at.is_(None),
        )
        .first()
    )
    if already_out:
        raise HTTPException(status_code=409, detail="This member already has this book checked out")

    now = datetime.utcnow()
    loan = models.Loan(
        book_id=payload.book_id,
        member_id=payload.member_id,
        borrowed_at=now,
        due_date=now + timedelta(days=payload.loan_days),
    )
    book.available_copies -= 1

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan