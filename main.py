from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import uvicorn

from import_wireframes import import_wireframes
from models import Wireframe
from database import SessionLocal
from routers import wireframe, comment, upload, checker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-startup: always import wireframes
    print("[LIFESPAN] Importing wireframes from CSV…")
    import_wireframes()

    yield  # Application runs

    # Post-shutdown cleanup (optional)
    try:
        SessionLocal().close()
    except Exception as e:
        print(f"[LIFESPAN] Error closing DB session: {e}")

app = FastAPI(lifespan=lifespan)

# Allow any front‑end origin (adjust in production as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded PDFs
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# API Routers
app.include_router(comment.router)
app.include_router(wireframe.router)
app.include_router(upload.router)
app.include_router(checker.router)

@app.get("/v01/")
def health_check():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
