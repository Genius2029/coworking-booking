from sqlmodel import SQLModel, Field

class Workspace(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    coworking_id: int = Field(foreign_key="coworking.id")
    name: str
    type: str
    price_per_hour: float
    capacity: int