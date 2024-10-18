from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    name: str
    description: Optional[str] = ""
    text: Optional[str] = ""


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int

    class Config:
        orm_mode = True
