from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import wireframe, comment, upload
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'uploads' folder exists
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register routers
app.include_router(comment.router)
app.include_router(wireframe.router)
app.include_router(upload.router)

@app.get("/v01/")
def root():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)