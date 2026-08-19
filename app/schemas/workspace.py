from pydantic import BaseModel

class WorkspaceCreate(BaseModel):
    name: str
    type: str
    price_per_hour: float
    capacity: int
