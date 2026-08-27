from datetime import datetime
from sqlmodel import select
from fastapi import APIRouter , Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.coworking import Coworking
from app.schemas.coworking import CoworkingCreate
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/coworking")
async def create_coworking(
    data: CoworkingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can create coworking")
    
    new_coworking = Coworking(
        name=data.name,
        address=data.address, 
        description=data.description,
        owner_id=current_user.id,
        created_at=str(datetime.now())
        )
    session.add(new_coworking)
    await session.commit()
    await session.refresh(new_coworking)
    return new_coworking

@router.get("/coworkings")
async def get_all_coworkings(session: AsyncSession = Depends(get_session)):
    query = select(Coworking)
    result = await session.execute(query)
    coworkings = result.scalars().all()
    return coworkings