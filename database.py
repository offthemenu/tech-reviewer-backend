from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Determine environment (Render sets this automatically)
IS_RENDER = os.environ.get("RENDER") == "true"

# Dynamic path based on environment
DATABASE_URL = (
    "sqlite:////data/reviewer.db" if IS_RENDER else "sqlite:///./reviewer.db"
)

# Set up engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Initialize tables if DB file doesn't exist
db_path = "/data/reviewer.db" if IS_RENDER else "./reviewer.db"
if not os.path.exists(db_path):
    Base.metadata.create_all(bind=engine)
