from datetime import datetime

import httpx
from sqlalchemy.orm import Session

from app.config.env_config import TELEGRAM_API_URL
from app.models import Client, OrderItem, Product
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.services.global_service import get_object_by_id
from app.services.message_service import escape_markdown


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


async def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")
    get_object_by_id(db, Client, order.client_id, "Client not found")

    older_status = db_order.status

    db_order.client_id = order.client_id
    db_order.status = order.status
    db_order.amount = order.amount
    db.commit()
    db.refresh(db_order)

    if (older_status != db_order.status):
        await notify_client_of_status_update(db_order)

    return db_order


async def notify_client_of_status_update(db_order: Order):
    chat_id = db_order.client.chat_id
    user_name = db_order.client.name

    escaped_user_name = escape_markdown(user_name)

    formatted_message = (
        f"Olá, *{escaped_user_name}*! 👋\n\n"
        f"🔄 O status do seu pedido foi atualizado para: *{db_order.status}*\n\n"
        f"Se precisar de mais alguma coisa, é só nos chamar! 💬\n"
        f"Obrigado por escolher nossa loja! 🙏💙"
    )

    payload = {
        'chat_id': chat_id,
        'text': formatted_message,
        'parse_mode': 'Markdown'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TELEGRAM_API_URL, params=payload)
        if response.status_code == 200:
            print(f"Message successfully sent to chat_id {chat_id}")
            print(f"\033[32mINFO:\033[0m     Order message successfully sent to chat_id {chat_id}")
        else:
            print(f"\033[91mERROR:\033[0m    Failed to send order message. Status code: "
                  f"{response.status_code}, Response: {response.text}")


def delete_order(db: Session, order_id: int):
    db_order = get_object_by_id(db, Order, order_id, "Order not found")

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted"}
