import asyncio
import re

import httpx
from sqlalchemy.orm import Session

from app.models import Client, User
from app.models.message_model import Message
from app.schemas.message_schema import MessageCreate
from app.services.global_service import get_object_by_id

from app.config.env_config import TELEGRAM_API_URL


def get_all_messages(db: Session):
    return db.query(Message).all()


def get_message(db: Session, message_id: int):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    return db_message


async def create_message(db: Session, message: MessageCreate):
    print(f"Creating message: {message}")
    if message.client_id is None:
        user = get_object_by_id(db, User, message.user_id, "User not found")
    else:
        client = get_object_by_id(db, Client, message.client_id, "Client not found")

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
        asyncio.run(send_to_bot(db_message, user.name))
    else:
        await send_to_client(db_message, client)
    return db_message


def escape_markdown(text: str) -> str:
    escape_chars = r"([_*\[\]()~`>#+\-=|{}.!])"
    return re.sub(escape_chars, r"\\\1", text)


async def send_to_bot(db_message: Message, name: str):
    chat_id = db_message.chat_id
    message = db_message.message
    user_name = name

    escaped_user_name = escape_markdown(user_name)
    escaped_message = escape_markdown(message)

    formatted_message = f"*{escaped_user_name}:*\n{escaped_message}"

    payload = {
        'chat_id': chat_id,
        'text': formatted_message,
        'parse_mode': 'Markdown'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TELEGRAM_API_URL, params=payload)
        if response.status_code == 200:
            print(f"Message successfully sent to chat_id {chat_id}")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")


async def send_to_client(db_message: Message, client: Client):
    from app.main import sio
    
    print(f"Message sent to client: {client}")
    await sio.emit("new_message_to_web", {
        "chat_id": db_message.chat_id,
        "message": db_message.message,
        "client": client
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
