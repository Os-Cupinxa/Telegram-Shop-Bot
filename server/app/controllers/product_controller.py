from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services import product_service
from app.config.database import get_db
from app.utils.access_token import get_current_user

router = APIRouter()


@router.get("/products/", response_model=List[ProductResponse], tags=["Products"])
def read_products(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return product_service.get_all_products(db)


@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return product_service.get_product(db, product_id)


@router.post("/products/", response_model=ProductResponse, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return product_service.create_product(db, product)


@router.put("/products/", response_model=ProductResponse, tags=["Products"])
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return product_service.update_product(db, product_id, product)


@router.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return product_service.delete_product(db, product_id)
