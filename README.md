# Coworking Booking API

A backend service for booking coworking spaces and workspaces (desks, meeting rooms) — built as a learning project to practice real-world backend architecture.

## Tech Stack
- **FastAPI** (fully async)
- **PostgreSQL** with **SQLModel** (async engine via SQLAlchemy)
- **JWT** authentication with **bcrypt** password hashing
- **Google Gemini API** for AI-powered workspace recommendations

## Features
- User registration & login (JWT-based auth)
- Role-based access (user / owner)
- Create coworkings and workspaces
- Book a workspace with automatic time-overlap validation
- Cancel bookings (soft delete via status field)
- View your own bookings only
- AI-powered workspace suggestions based on natural language queries (e.g. "quiet spot by the window")

## Architecture
- `models/` — SQLModel table definitions
- `schemas/` — Pydantic request/response schemas
- `routers/` — API endpoints grouped by entity
- `core/` — security (hashing, JWT) and AI integration
- `database.py` — async DB session management

## Running locally
1. Clone the repo
2. Create a `.env` file with `DATABASE_URL`, `SECRET_KEY`, and `GEMINI_API_KEY`
3. `pip install -r requirements.txt`
4. `python -m uvicorn app.main:app --reload`
5. Open `http://127.0.0.1:8000/docs` for interactive API docs

🔗 **Live demo:** https://coworking-booking-production-5b9d.up.railway.app/docs