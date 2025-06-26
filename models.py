from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Wireframe(Base):
    __tablename__ = "wireframes"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, index=True)
    device = Column(String)
    page_name = Column(String)
    page_path = Column(String)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String)
    device = Column(String)
    page_name = Column(String)
    page_path = Column(String)
    ui_component = Column(String)
    comment = Column(String)
    filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    wireframe_id = Column(Integer, ForeignKey("wireframes.id"))

