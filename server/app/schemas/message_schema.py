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


class MessageResponse(MessageBase):
    id: int
    user_id: Optional[int] = None
    client_id: Optional[int] = None

    class Config:
        orm_mode = True
