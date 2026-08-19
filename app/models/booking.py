from sqlmodel import SQLModel, Field

class Booking(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    workspace_id: int = Field(foreign_key="workspace.id")
    start_time: str
    end_time: str
    status: str