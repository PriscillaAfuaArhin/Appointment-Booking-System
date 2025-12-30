from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.routers.users import router as users_router
from backend.app.routers.services import router as services_router
from backend.app.routers.availability import router as availability_router
from backend.app.routers.slots import router as slots_router
from backend.app.routers.appointments import router as appointments_router




Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointment Booking System")
app.include_router(users_router)
app.include_router(services_router)
app.include_router(availability_router)
app.include_router(slots_router)
app.include_router(appointments_router)




