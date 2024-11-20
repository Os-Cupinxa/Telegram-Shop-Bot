from pydantic import BaseModel
from typing import Optional

from app.schemas.category_schema import CategoryResponse


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
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
