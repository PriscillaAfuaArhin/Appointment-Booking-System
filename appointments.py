from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.app.database import SessionLocal
from backend.app import models

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_appointment(
    provider_id: int,
    service_id: int,
    start_time: datetime,
    db: Session = Depends(get_db)
):
    # 1. Get service duration
    service = db.query(models.Service).filter(
        models.Service.service_id == service_id
    ).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    end_time = start_time + timedelta(minutes=service.duration_minutes)

    # 2. Check for overlapping appointments
    conflict = db.query(models.Appointment).filter(
        models.Appointment.provider_id == provider_id,
        models.Appointment.start_time < end_time,
        models.Appointment.end_time > start_time
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="Time slot already booked")

    # 3. Create appointment
    appointment = models.Appointment(
        provider_id=provider_id,
        service_id=service_id,
        start_time=start_time,
        end_time=end_time,
        status="BOOKED"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

@router.get("/my")
def my_appointments(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return db.query(models.Appointment).filter(
        models.Appointment.customer_id == customer_id
    ).order_by(models.Appointment.start_time.desc()).all()

@router.patch("/{appointment_id}/confirm")
def confirm_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.appointment_id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "CONFIRMED"
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/provider/{provider_id}")
def provider_schedule(
    provider_id: int,
    db: Session = Depends(get_db)
):
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.provider_id == provider_id)
        .order_by(models.Appointment.start_time)
        .all()
    )
    return appointments

@router.patch("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(models.Appointment).get(appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "CANCELLED"
    db.commit()
    return {"message": "Appointment cancelled"}

@router.patch("/{appointment_id}/complete")
def complete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(models.Appointment).get(appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "COMPLETED"
    db.commit()
    return {"message": "Appointment completed"}

@router.get("/provider/{provider_id}")
def get_provider_schedule(
    provider_id: int,
    db: Session = Depends(get_db)
):
    appointments = db.query(models.Appointment).filter(
        models.Appointment.provider_id == provider_id
    ).all()

    return [
        {
            "id": a.appointment_id,
            "title": f"Service {a.service_id} ({a.status})",
            "start": a.start_time,
            "end": a.end_time,
            "status": a.status
        }
        for a in appointments
    ]
