from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderItemBase, OrderItemResponse, OrderUpdate
from app.services import order_service
from app.config.database import get_db
from app.utils.access_token import get_current_user

router = APIRouter()


@router.get("/orders/", response_model=List[OrderResponse], tags=["Orders"])
def read_orders(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return order_service.get_all_orders(db)


@router.get("/orders/client/{client_id}", response_model=List[OrderResponse], tags=["Orders"])
def read_orders_by_client(client_id: int, db: Session = Depends(get_db)):
    return order_service.get_order_by_client(db, client_id)


@router.get("/orders/items/{order_id}", response_model=List[OrderItemResponse], tags=["Orders"])
def read_items_by_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_items_by_order(db, order_id)


@router.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def read_order(order_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return order_service.get_order(db, order_id)


@router.post("/orders/", response_model=OrderResponse, tags=["Orders"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)


@router.put("/orders/", response_model=OrderResponse, tags=["Orders"])
async def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return await order_service.update_order(db, order_id, order)


@router.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return order_service.delete_order(db, order_id)
