from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Comment, Wireframe
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/v01")

# Schema for input
class CommentSchema(BaseModel):
    project: str
    device: str
    page_name: str
    page_path: str
    ui_component: str
    comment: str
    filename: str

# Schema for output
class CommentOut(CommentSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

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

@router.post("/add_comment", status_code=200)
def add_comment(payload: CommentSchema, db: Session = Depends(get_db)):
    wireframe_record = db.query(Wireframe).filter_by(page_name=payload.page_name).first()
    if not wireframe_record:
        raise HTTPException(status_code=400, detail="No wireframe found for that page")

    new_comment = Comment(**payload.model_dump(), wireframe_id=wireframe_record.id)
    db.add(new_comment)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to add comment: {e}")
    
    db.refresh(new_comment)
    return new_comment
    

@router.get("/comments", response_model=List[CommentOut], status_code=200)
def get_all_comments(
    project: str,
    device: str,
    db: Session = Depends(get_db),
):
    try:
        comments = (
            db.query(Comment)
            .filter(Comment.project == project, Comment.device == device)
            .order_by(Comment.created_at.desc())
            .all()
        )
        return comments
    except Exception as e:
        print(f"[ERROR] Failed to get comments: {e}")
        raise HTTPException(status_code=400, detail="Failed to get comments")


@router.delete("/comment/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    try:
        c = db.get(Comment, comment_id)
        if not c:
            raise HTTPException(status_code=404, detail="Comment not found")
        db.delete(c)
        db.commit()
    except Exception as e:
        print(f"[ERROR] Failed to delete comment: {e}")
        raise HTTPException(status_code=400, detail="Failed to delete comment")