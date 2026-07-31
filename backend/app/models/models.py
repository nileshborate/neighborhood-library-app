from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, ForeignKey, Numeric
from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    genre = Column(String(100), nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("total_copies >= 0", name="ck_books_total_copies_nonneg"),
        CheckConstraint("available_copies >= 0", name="ck_books_available_copies_nonneg"),
        CheckConstraint("available_copies <= total_copies", name="ck_books_available_le_total"),
    )

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="RESTRICT"), nullable=False)

    borrowed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)  # NULL = still borrowed

    fine_amount = Column(Numeric(10, 2), nullable=False, default=0)