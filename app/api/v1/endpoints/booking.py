from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import and_, select

from app.api.v1.deps import get_current_user, get_db
from app.db.models.booking import Booking, Resource

router = APIRouter()


class ResourceCreate(BaseModel):
    name: str


class ResourceOut(BaseModel):
    id: str
    name: str


class BookingCreate(BaseModel):
    resource_id: str
    start_at: datetime
    end_at: datetime


class BookingOut(BaseModel):
    id: str
    resource_id: str
    start_at: datetime
    end_at: datetime
    status: str


@router.post("/booking/resources", response_model=ResourceOut)
async def create_resource(payload: ResourceCreate, db=Depends(get_db), _=Depends(get_current_user)):
    r = Resource(name=payload.name)
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return ResourceOut(id=str(r.id), name=r.name)


@router.get("/booking/resources", response_model=list[ResourceOut])
async def list_resources(db=Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Resource).order_by(Resource.created_at.desc()))
    rows = result.scalars().all()
    return [ResourceOut(id=str(r.id), name=r.name) for r in rows]


@router.post("/booking/bookings", response_model=BookingOut)
async def create_booking(payload: BookingCreate, db=Depends(get_db), _=Depends(get_current_user)):
    if payload.end_at <= payload.start_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid time range")

    try:
        resource_uuid = uuid.UUID(payload.resource_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resource_id")

    # Overlap check: (start < existing_end) AND (end > existing_start)
    overlap = and_(
        Booking.resource_id == resource_uuid,
        Booking.status == "confirmed",
        payload.start_at < Booking.end_at,
        payload.end_at > Booking.start_at,
    )
    result = await db.execute(select(Booking).where(overlap).limit(1))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Time slot unavailable")

    b = Booking(resource_id=resource_uuid, start_at=payload.start_at, end_at=payload.end_at, status="confirmed")
    db.add(b)
    await db.commit()
    await db.refresh(b)
    return BookingOut(
        id=str(b.id),
        resource_id=str(b.resource_id),
        start_at=b.start_at,
        end_at=b.end_at,
        status=b.status,
    )


@router.get("/booking/bookings", response_model=list[BookingOut])
async def list_bookings(resource_id: str | None = None, db=Depends(get_db), _=Depends(get_current_user)):
    q = select(Booking).order_by(Booking.created_at.desc())
    if resource_id:
        q = q.where(Booking.resource_id == uuid.UUID(resource_id))
    result = await db.execute(q)
    rows = result.scalars().all()
    return [
        BookingOut(
            id=str(b.id),
            resource_id=str(b.resource_id),
            start_at=b.start_at,
            end_at=b.end_at,
            status=b.status,
        )
        for b in rows
    ]

