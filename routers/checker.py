from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/debug/check-db")
def check_db_file():
    path = "/data/reviewer.db"
    return {
        "exists": os.path.exists(path),
        "size_bytes": os.path.getsize(path) if os.path.exists(path) else 0
    }
