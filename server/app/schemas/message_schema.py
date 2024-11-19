from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageBase(BaseModel):
    chat_id: int
    message: str
    created_date: datetime


class MessageCreate(MessageBase):
    user_id: Optional[int] = None
    client_id: Optional[int] = None
    created_date: datetime = datetime.now()


class MessageResponse(MessageBase):
    id: int
    user_id: Optional[int] = None
    client_id: Optional[int] = None
    status: str

    class Config:
        orm_mode = True
