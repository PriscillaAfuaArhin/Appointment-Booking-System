from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app import models

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_service(
    provider_id: int,
    duration_minutes: int,
    db: Session = Depends(get_db)
):
    service = models.Service(
        provider_id=provider_id,
        duration_minutes=duration_minutes
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


from fastapi import FastAPI
from backend.app.database import Base, engine
from backend.app.routers import availability, slots, services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointment Booking System")

app.include_router(availability.router)
app.include_router(services.router)
app.include_router(slots.router)
