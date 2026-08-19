from pydantic import BaseModel

class CoworkingCreate(BaseModel):
    name: str
    address: str
    description: str