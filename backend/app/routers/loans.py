from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/api/loans", tags=["loans"])
FINE_PER_DAY = 10 

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

@router.post("/{loan_id}/return", response_model=schemas.LoanOut)
def return_book(loan_id: int, payload: schemas.LoanReturn, db: Session = Depends(get_db)):
    loan = (
        db.query(models.Loan)
        .options(joinedload(models.Loan.book), joinedload(models.Loan.member))
        .filter(models.Loan.id == loan_id)
        .first()
    )
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.returned_at is not None:
        raise HTTPException(status_code=400, detail="This book has already been returned")

    returned_at = payload.returned_at or datetime.utcnow()
    loan.returned_at = returned_at

    if returned_at > loan.due_date:
        overdue_days = (returned_at.date() - loan.due_date.date()).days
        loan.fine_amount = FINE_PER_DAY * overdue_days

    loan.book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return loan

@router.get("", response_model=List[schemas.LoanOut])
def list_loans(
    member_id: Optional[int] = Query(None),
    book_id: Optional[int] = Query(None),
    active_only: bool = Query(False, description="Only currently-borrowed (not yet returned) loans"),
    overdue_only: bool = Query(False, description="Only active loans past their due date"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Loan).options(
        joinedload(models.Loan.book), joinedload(models.Loan.member)
    )

    if member_id is not None:
        query = query.filter(models.Loan.member_id == member_id)
    if book_id is not None:
        query = query.filter(models.Loan.book_id == book_id)
    if active_only or overdue_only:
        query = query.filter(models.Loan.returned_at.is_(None))
    if overdue_only:
        query = query.filter(models.Loan.due_date < datetime.utcnow())

    return query.order_by(models.Loan.borrowed_at.desc()).all()