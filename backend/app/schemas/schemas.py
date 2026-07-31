from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=20)
    genre: Optional[str] = Field(None, max_length=100)
    total_copies: int = Field(1, ge=0)


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: Optional[str]
    genre: Optional[str]
    total_copies: int
    available_copies: int
    created_at: datetime