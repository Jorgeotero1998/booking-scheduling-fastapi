# OteroScheduler

**EN**: Booking & Scheduling (overlap-safe)  
**ES**: Reservas y scheduling (sin solapamientos)

## Live demo / Demo online
- **Web**: https://booking-scheduling-fastapi.vercel.app
- **API docs**: https://booking-scheduling-fastapi-api.onrender.com/docs
- **API health**: https://booking-scheduling-fastapi-api.onrender.com/api/v1/health

## Stack
- FastAPI
- PostgreSQL
- Docker
- Concurrency rules

## Local setup (Docker)

`ash
cp .env.example .env
docker compose up --build
`

## Credentials (demo)

**EN**: Default demo admin is seeded from ADMIN_EMAIL / ADMIN_PASSWORD.  
**ES**: El admin demo se crea desde ADMIN_EMAIL / ADMIN_PASSWORD.

## Deploy

**EN**:
- Backend: Render (Blueprint via ender.yaml)
- Frontend: Vercel (Root Directory: web)

**ES**:
- Backend: Render (Blueprint con ender.yaml)
- Frontend: Vercel (Root Directory: web)
