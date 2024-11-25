from typing import List

from pydantic import BaseModel
from datetime import datetime

from app.schemas.product_schema import ProductResponse


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int
    product: ProductResponse


class OrderBase(BaseModel):
    client_id: int
    status: str
    amount: float


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderUpdate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
