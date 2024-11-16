import asyncio

from sqlalchemy.orm import Session

from app.models.message_model import Message
from app.schemas.message_schema import MessageCreate
from app.services.global_service import get_object_by_id


def get_all_messages(db: Session):
    return db.query(Message).all()


def get_message(db: Session, message_id: int):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    return db_message


def create_message(db: Session, message: MessageCreate):
    db_message = Message(
        chat_id=message.chat_id,
        created_date=message.created_date,
        message=message.message,
        user_id=message.user_id,
        client_id=message.client_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    if message.client_id is None:
        asyncio.run(send_to_bot(db_message))
    else:
        asyncio.run(send_to_client(db_message))

    return db_message


async def send_to_bot(db_message: Message):
    from app.main import sio
    await sio.emit("new_message_to_bot", {
        "chat_id": db_message.chat_id,
        "message": db_message.message,
        "user_id": db_message.user_id
    })

async def send_to_client(db_message: Message):
    from app.main import sio
    await sio.emit("new_message_to_web", {
        "chat_id": db_message.chat_id,
        "message": db_message.message,
        "client_id": db_message.user_id
    })


def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    db_message.message = message.message
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    db.delete(db_message)
    db.commit()
    return {"message": "Message deleted"}
