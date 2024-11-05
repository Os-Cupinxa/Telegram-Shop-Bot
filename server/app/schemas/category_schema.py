from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    emoji: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
