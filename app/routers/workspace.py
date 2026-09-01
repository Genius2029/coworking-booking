from fastapi import APIRouter , Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate

router = APIRouter()


@router.post("/coworkings/{coworkings_id}/workspaces")
async def create_workspace(coworking_id: int, data: WorkspaceCreate, session: AsyncSession = Depends(get_session)):
    new_workspace = Workspace(
        coworking_id=coworking_id,
        name=data.name,
        type=data.type,
        price_per_hour=data.price_per_hour,
        capacity=data.capacity,
        description=data.description
    )
    session.add(new_workspace)
    await session.commit()
    await session.refresh(new_workspace)
    return new_workspace

@router.get("/workspaces")
async def get_all_workspaces(session: AsyncSession = Depends(get_session)):
    query = select(Workspace)
    result = await session.execute(query)
    workspaces = result.scalars().all()
    return workspaces
