from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from backend.app.database import SessionLocal
from backend.app import models

router = APIRouter(
    prefix="/slots",
    tags=["Slots"]
)

# -----------------------------
# Database dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Generate available slots
# -----------------------------
@router.get("/")
def get_available_slots(
    provider_id: int,
    service_id: int,
    date: date,
    db: Session = Depends(get_db)
):
    """
    Returns all available appointment slots for:
    - a provider
    - a service
    - a specific date
    """

    # 1. Get service duration
    service = (
        db.query(models.Service)
        .filter(
            models.Service.service_id == service_id,
            models.Service.provider_id == provider_id
        )
        .first()
    )

    if not service:
        return {"error": "Service not found"}

    duration = timedelta(minutes=service.duration_minutes)

    # 2. Get availability for that weekday
    weekday = date.weekday()  # Monday = 0

    availability = (
        db.query(models.Availability)
        .filter(
            models.Availability.provider_id == provider_id,
            models.Availability.day_of_week == weekday
        )
        .first()
    )

    if not availability:
        return []

    # 3. Build datetime range
    start_datetime = datetime.combine(date, availability.start_time)
    end_datetime = datetime.combine(date, availability.end_time)

    # 4. Fetch existing appointments
    existing_appointments = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.provider_id == provider_id,
            models.Appointment.start_time >= start_datetime,
            models.Appointment.end_time <= end_datetime
        )
        .all()
    )

    booked_slots = [
        (appt.start_time, appt.end_time)
        for appt in existing_appointments
    ]

    # 5. Generate slots
    slots = []
    current_time = start_datetime

    while current_time + duration <= end_datetime:
        slot_end = current_time + duration

        # Check overlap
        overlap = False
        for booked_start, booked_end in booked_slots:
            if not (slot_end <= booked_start or current_time >= booked_end):
                overlap = True
                break

        if not overlap:
            slots.append({
                "start": current_time,
                "end": slot_end
            })

        current_time += duration

    return slots
