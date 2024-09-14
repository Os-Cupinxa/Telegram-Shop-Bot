from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    category_id: Optional[int] = None
    photo_url: str
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
