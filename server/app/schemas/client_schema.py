from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    phone_number: str
    city: str
    address: str
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True
