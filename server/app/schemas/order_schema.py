from typing import List

from pydantic import BaseModel
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    client_id: int
    status: str
    amount: int


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderResponse(OrderBase):
    id: int
    created_date: datetime
    items: List[OrderItemBase]

    class Config:
        orm_mode = True
