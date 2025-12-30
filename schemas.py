from pydantic import BaseModel
from datetime import time


class AvailabilityCreate(BaseModel):
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time


class UserCreate(BaseModel):
    email: str
    role: str

class UserResponse(UserCreate):
    user_id: int

class Config:
    from_attributes = True
