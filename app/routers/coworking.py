from datetime import datetime
from fastapi import APIRouter , Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.coworking import Coworking
from app.schemas.coworking import CoworkingCreate

router = APIRouter()


@router.post("/coworking")
async def create_coworking(data: CoworkingCreate, session: AsyncSession = Depends(get_session)):
    new_coworking = Coworking(
        name=data.name,
        address=data.address, 
        description=data.description,
        owner_id=1,
        created_at=str(datetime.now())
        )
    session.add(new_coworking)
    await session.commit()
    await session.refresh(new_coworking)
    return new_coworking

