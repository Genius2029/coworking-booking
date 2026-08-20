from pydantic import BaseModel

class BookingCreate(BaseModel):
    start_time: str
    end_time: str