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
        from_attributes = True

class ConversationResponse(BaseModel):
    chat_id: int
    last_message: str
    last_message_date: datetime
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
