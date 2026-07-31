from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import models  
from app.routers import books, members, loans

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Neighborhood Library API")

app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}