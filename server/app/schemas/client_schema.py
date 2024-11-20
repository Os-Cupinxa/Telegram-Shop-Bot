from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    cpf: str
    phone_number: str
    city: str
    address: str
    chat_id: int
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True
