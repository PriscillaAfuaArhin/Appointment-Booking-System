from sqlalchemy import Column, Integer, String, Time, DateTime
from backend.app.database import Base
from .database import Base

class Availability(Base):
    __tablename__ = "availability"

    availability_id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, index=True)
    day_of_week = Column(Integer)  # 0 = Sunday, 6 = Saturday
    start_time = Column(Time)
    end_time = Column(Time)


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, index=True)
    duration_minutes = Column(Integer)


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, index=True)
    service_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)  # "customer" or "provider"
