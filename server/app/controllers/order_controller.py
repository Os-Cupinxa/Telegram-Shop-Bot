from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services import order_service
from app.config.database import get_db

router = APIRouter()


@router.get("/orders/", response_model=List[OrderResponse], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return order_service.get_all_orders(db)


@router.get("/orders/client/{client_id}", response_model=List[OrderResponse], tags=["Orders"])
def read_orders_by_client(client_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_by_client(db, client_id)


@router.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)


@router.post("/orders/", response_model=OrderResponse, tags=["Orders"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)


@router.put("/orders/", response_model=OrderResponse, tags=["Orders"])
def update_order(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.update_order(db, order_id, order)


@router.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.delete_order(db, order_id)
