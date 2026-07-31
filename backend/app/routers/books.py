from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/api/books", tags=["books"])


@router.post("", response_model=schemas.BookOut, status_code=201)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    if payload.isbn:
        existing = db.query(models.Book).filter(models.Book.isbn == payload.isbn).first()
        if existing:
            raise HTTPException(status_code=409, detail="A book with this ISBN already exists")

    book = models.Book(
        title=payload.title,
        author=payload.author,
        isbn=payload.isbn,
        genre=payload.genre,
        total_copies=payload.total_copies,
        available_copies=payload.total_copies,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("", response_model=List[schemas.BookOut])
def list_books(
    q: Optional[str] = Query(None, description="Search by title or author"),
    available_only: bool = Query(False),
    db: Session = Depends(get_db),
):
    query = db.query(models.Book)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(models.Book.title.ilike(like), models.Book.author.ilike(like)))
    if available_only:
        query = query.filter(models.Book.available_copies > 0)
    return query.order_by(models.Book.title).all()

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = payload.model_dump(exclude_unset=True)

    if "total_copies" in data:
        currently_borrowed = book.total_copies - book.available_copies
        if data["total_copies"] < currently_borrowed:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot set total_copies below the {currently_borrowed} copies currently on loan",
            )
        book.available_copies = data["total_copies"] - currently_borrowed

    for field, value in data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book