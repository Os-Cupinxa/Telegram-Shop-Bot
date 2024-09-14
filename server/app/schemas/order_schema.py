from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    client_id: int
    status: str
    amount: int


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True
