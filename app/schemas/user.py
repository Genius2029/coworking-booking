from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str 
    full_name: str 
    password: str
    role: str

class UserRead(BaseModel):
    id: int
    email: str
    full_name: str
    role: str