from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Client
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(and_(Order.id == order_id)).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


def create_order(db: Session, order: OrderCreate):
    client = db.query(Client).filter(and_(Client.id == order.client_id)).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db_order = Order(
        client_id=order.client_id,
        created_date=datetime.now(),
        status=order.status,
        amount=order.amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: OrderCreate):
    db_order = db.query(Order).filter(and_(Order.id == order_id)).first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.client_id = order.client_id
    db_order.status = order.status
    db_order.amount = order.amount
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(and_(Order.id == order_id)).first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted"}
