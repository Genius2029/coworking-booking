from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select
from datetime import datetime

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=data.role,
        created_at=str(datetime.now())
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login")
async def login(email: str, password: str, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.first()

    if not user or not verify_password(password, user[0].hashed_password):
        raise HTTPException(status_code=401, detail="invalid email or password")

    token = create_access_token(user_id=user[0].id)
    return {"access_token": token, "token_type": "bearer"}
