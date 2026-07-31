from fastapi import APIRouter, Depends, HTTPException
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