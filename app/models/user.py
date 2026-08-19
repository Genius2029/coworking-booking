from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str 
    hashed_password: str
    full_name: str
    role: str
    created_at: str