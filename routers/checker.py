from fastapi import APIRouter
import os

router = APIRouter(prefix="/v01")

@router.get("/debug/check-db")
def check_db_file():
    path = "/data/reviewer.db"
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    return {"exists": exists, "size_bytes": size}
