from sqlmodel import SQLModel, Field

class Coworking(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    name: str
    address: str
    description: str
    created_at: str

