
# Appointment Booking System (ABS)

##  Overview
The Appointment Booking System (ABS) is a web-based application designed to automate appointment scheduling for small service businesses. It provides a customer-facing interface for booking appointments and a provider-facing system for managing services, availability, and appointments. The goal is to replace manual booking methods (phone calls, emails) with a simple, self-service platform.

This project is implemented as a **Minimum Viable Product (MVP)**.

---

##  Features

### Customer Features
- View available appointment slots
- Book appointments for selected services
- View appointment status

### Provider Features
- Create and manage services
- Set weekly availability
- View scheduled appointments
- Cancel appointments

### System Features
- RESTful API built with FastAPI
- PostgreSQL database
- Swagger UI for API testing
- Automatic slot generation based on availability
- Minimal HTML frontend

---

##  Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **API Documentation:** Swagger (OpenAPI)
- **Tools:** VS Code, pgAdmin

---

##  Project Structure
PROJECT/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       └── routers/
│           ├── availability.py
│           ├── services.py
│           ├── slots.py
│           ├── appointments.py
│           └── users.py
│
├── frontend/
│   ├── index.html
│   └── book.html
│
├── appointments.db (optional SQLite testing)

