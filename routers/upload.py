from fastapi import APIRouter, UploadFile, File
import os
import shutil
from pathlib import Path
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/v01")

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"


@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        filename = file.filename
        filepath = os.path.join("uploads", filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(status_code=200, content={"filename": filename})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

