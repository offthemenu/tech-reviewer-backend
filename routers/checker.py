from fastapi import APIRouter, Depends
import os
from database import SessionLocal
from models import Wireframe

router = APIRouter(prefix="/v01")

def get_db():
    """
    FastAPI dependency to provide a database session.

    Yields a database session that should be used as a context manager.
    The session is closed after the context manager is exited.
    """
    db = SessionLocal()
    try:
        print("Database session is being closed.")
        yield db
    finally:
        db.close()

@router.get("/debug/check-db")
def check_db_file():
    path = "/data/reviewer.db"
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    return {"exists": exists, "size_bytes": size}

@router.get("/debug/count-wireframes")
def count_wires(db = Depends(get_db)):
    return {"count": db.query(Wireframe).count()}
