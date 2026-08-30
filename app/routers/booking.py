from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_current_user
from app.models.user import User

from app.database import get_session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

router = APIRouter()


@router.post("/workspaces/{workspace_id}/bookings")
async def create_booking(
    workspace_id: int,
    data: BookingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    if data.start_time >= data.end_time:
        raise HTTPException(status_code=400, detail="The start time must be earlier than the end time")
    
    query = select(Booking).where(
        Booking.workspace_id == workspace_id,
        Booking.start_time < data.end_time,
        Booking.end_time > data.start_time
    )
    result = await session.execute(query)
    conflicting_booking = result.first()

    if conflicting_booking:
        raise HTTPException(status_code=400, detail="This time is already taken")

    new_booking = Booking(
        workspace_id=workspace_id,
        user_id=current_user.id,
        start_time=data.start_time,
        end_time=data.end_time,
        status="active"
    )
    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)
    return new_booking

@router.get("/bookings")
async def get_all_bookings(current_user: User = Depends(get_current_user), session = Depends(get_session)):
    query = select(Booking).where(
        Booking.user_id == current_user.id,
    )
    result = await session.execute(query)
    bookings = result.scalars().all()
    return bookings

@router.patch("/bookings/{booking_id}/cancel")
async def cancel_bookings(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Booking).where(Booking.id == booking_id)
    result = await session.execute(query)
    booking = result.first()

    if not booking:
        raise HTTPException(status_code=404, detail="It's not finded")

    booking = booking[0]

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your booking")

    booking.status = "cancelled"
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking
