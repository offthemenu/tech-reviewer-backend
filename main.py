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
    # Runs before the app starts
    db = SessionLocal()
    try:
        if db.query(Wireframe).count() == 0:
            print("[LIFESPAN] No wireframes found in DB. Importing from CSV.")
            import_wireframes()
        else:
            print("[LIFESPAN] Wireframes already present.")
    finally:
        db.close()

    yield  # App runs after this
    # Runs after the app is shut down
    db = SessionLocal()
    try:
        db.dispose()
    except Exception as e:
        print(f"[LIFESPAN] Failed to dispose db session: {e}")
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(comment.router)
app.include_router(wireframe.router)
app.include_router(upload.router)
app.include_router(checker.router)

# Health check
@app.get("/v01/")
def root():
    return {"message": "Backend is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
