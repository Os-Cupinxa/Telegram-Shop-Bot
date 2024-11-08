from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Client, OrderItem
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate
from app.services.global_service import get_object_by_id


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")

    return db_order


def create_order(db: Session, order: OrderCreate):
    get_object_by_id(db, Client, order.client_id, "Client not found")

    db_order = Order(
        client_id=order.client_id,
        created_date=datetime.now(),
        status=order.status,
        amount=order.amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)

    return db_order


def update_order(db: Session, order_id: int, order: OrderCreate):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")
    get_object_by_id(db, Client, order.client_id, "Client not found")

    db_order.client_id = order.client_id
    db_order.status = order.status
    db_order.amount = order.amount
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted"}
