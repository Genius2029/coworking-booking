from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.database import engine
from app.models.user import User

from app.models.coworking import Coworking
from app.models.workspace import Workspace
from app.models.booking import Booking

from app.routers.user import router as user_router
from app.routers.coworking import router as coworking_router
from app.routers.workspace import router as workspace_router
from app.routers.booking import router as booking_router
from app.routers.ai import router as ai_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
#join to routers Into main 
app.include_router(user_router)#register/login router
app.include_router(coworking_router)
app.include_router(workspace_router)
app.include_router(booking_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "Coworking booking API is running"}