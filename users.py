from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app import models, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        email=user.email,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
