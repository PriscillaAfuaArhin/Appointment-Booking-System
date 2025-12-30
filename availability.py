from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app import models
from backend.app.schemas import AvailabilityCreate

router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_availability(
    availability: AvailabilityCreate,   # ✅ BODY
    db: Session = Depends(get_db)
):
    record = models.Availability(
        provider_id=availability.provider_id,
        day_of_week=availability.day_of_week,
        start_time=availability.start_time,
        end_time=availability.end_time
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
