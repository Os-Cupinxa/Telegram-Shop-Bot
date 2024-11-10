from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Client, OrderItem, Product
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate
from app.services.global_service import get_object_by_id


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")

    return db_order


def get_order_by_client(db: Session, client_id: int):
    orders = db.query(Order).filter(Order.client_id == client_id).all()

    return orders


def get_items_by_order(db: Session, order_id: int):
    items_with_products = (
        db.query(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    items = [
        {
            "item_id": order_item.id,
            "quantity": order_item.quantity,
            "product": product
        }
        for order_item, product in items_with_products
    ]

    return items


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
