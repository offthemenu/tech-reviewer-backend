from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Wireframe
from pydantic import BaseModel

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

class WireframeSchema(BaseModel):
    project: str
    device: str
    page_name: str
    page_path: str

@router.post("/add_wireframe")
def add_wireframe(payload: WireframeSchema, db: Session = Depends(get_db)):
    """
    Add a new wireframe to the database.

    Returns the newly added wireframe.
    """
    if not payload:
        raise ValueError("No payload provided")

    try:
        new_wireframe = Wireframe(**payload.model_dump())
    except TypeError as e:
        raise ValueError(f"Invalid payload: {e}")

    if not new_wireframe:
        raise ValueError("Failed to create wireframe")

    db.add(new_wireframe)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    db.refresh(new_wireframe)
    return new_wireframe


@router.get("/wireframe")
def get_dropdown_data(db: Session = Depends(get_db)):
    """
    Return data for dropdowns in the frontend.

    Returns a JSON object with the following structure:

    * projects: a list of strings representing the projects
    * devices_by_project: an object mapping project names to lists of
      string device names
    * pages_by_project_device: an object mapping `(project_name, device_name)`
      tuples to lists of objects with `name` and `path` fields
    """
    all_wireframes = db.query(Wireframe).all()

    if not all_wireframes:
        raise ValueError("No wireframes found")

    projects = set()
    devices_by_project = {}
    pages_by_project_device = {}

    for wf in all_wireframes:
        if not wf.project:
            raise ValueError("Project name is null")
        if not wf.device:
            raise ValueError("Device name is null")
        if not wf.page_name:
            raise ValueError("Page name is null")
        if not wf.page_path:
            raise ValueError("Page path is null")

        project = wf.project
        device = wf.device
        page_name = wf.page_name
        page_path = wf.page_path

        # Project list
        projects.add(project)

        # Devices per project
        if project not in devices_by_project:
            devices_by_project[project] = set()
        devices_by_project[project].add(device)

        # Pages per (project, device)
        key = (project, device)
        if key not in pages_by_project_device:
            pages_by_project_device[key] = []
        pages_by_project_device[key].append({
            "name": page_name,
            "path": page_path
        })

    # Convert sets to lists for output
    devices_cleaned = {}
    for proj, device_set in devices_by_project.items():
        devices_cleaned[proj] = sorted(list(device_set))

    pages_cleaned = {}
    for (proj, dev), page_list in pages_by_project_device.items():
        pages_cleaned[f"{proj}_{dev}"] = page_list

    return {
        "projects": sorted(list(projects)),
        "devices_by_project": devices_cleaned,
        "pages_by_project_device": pages_cleaned
    }
