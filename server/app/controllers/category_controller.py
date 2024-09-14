from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.services import category_service
from app.config.database import get_db

router = APIRouter()


@router.get("/categories/", response_model=List[CategoryResponse], tags=["Categories"])
def read_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)


@router.get("/categories/{category_id}", response_model=CategoryResponse, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)


@router.post("/categories/", response_model=CategoryResponse, tags=["Categories"])
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)


@router.put("/categories/", response_model=CategoryResponse, tags=["Categories"])
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.update_category(db, category_id, category)


@router.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)
