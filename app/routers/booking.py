from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

router = APIRouter()


@router.post("/workspaces/{workspace_id}/bookings")
async def create_booking(workspace_id: int, data: BookingCreate, session: AsyncSession = Depends(get_session)):
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
        user_id=1,
        start_time=data.start_time,
        end_time=data.end_time,
        status="active"
    )
    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)
    return new_booking