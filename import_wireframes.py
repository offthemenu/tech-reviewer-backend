import csv
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Wireframe, Base

CSV_PATH = "data/sample_wireframe_data.csv"  # or pass a new filename

def import_wireframes(csv_file: str = CSV_PATH):
    if not os.path.exists(csv_file):
        print(f"[ERROR] File not found: {csv_file}")
        return

    # Ensure DB tables exist
    Base.metadata.create_all(bind=engine)

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    db: Session = SessionLocal()

    try:
        inserted = 0
        for row in records:
            exists = db.query(Wireframe).filter_by(
                project=row["project"],
                device=row["device"],
                page_name=row["page_name"],
                page_path=row["page_path"]
            ).first()

            if not exists:
                new_wireframe = Wireframe(
                    project=row["project"],
                    device=row["device"],
                    page_name=row["page_name"],
                    page_path=row["page_path"]
                )
                db.add(new_wireframe)
                inserted += 1

        db.commit()
        print(f"[INFO] Imported {inserted} new wireframe rows.")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to import: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_wireframes()
