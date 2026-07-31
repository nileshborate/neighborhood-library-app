from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import models  # noqa: F401  registers Book with Base.metadata
from app.routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Neighborhood Library API")

app.include_router(books.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}