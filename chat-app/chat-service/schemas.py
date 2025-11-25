from pydantic import BaseModel

class MessageCreate(BaseModel):
    room_id: str
    sender: str
    content: str

class MessageResponse(BaseModel):
    id: int
    room_id: str
    sender: str
    content: str

    class Config:
        orm_mode = True