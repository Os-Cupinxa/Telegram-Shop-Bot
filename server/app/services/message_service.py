import asyncio
import re

import httpx
from sqlalchemy.orm import Session

from app.models import Client, User
from app.models.message_model import Message
from app.schemas.message_schema import MessageCreate
from app.services.global_service import get_object_by_id

from app.config.env_config import TELEGRAM_API_URL
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload
from typing import Optional


def get_all_messages(db: Session, chat_id: Optional[int] = None):
    query = db.query(Message)
    if chat_id:
        query = query.filter(Message.chat_id == chat_id)
    return query.order_by(Message.created_date).all()



def get_message(db: Session, message_id: int):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    return db_message


async def create_message_Web(db: Session, message: MessageCreate, user_id: int):
    if message.client_id is None:
        user = get_object_by_id(db, User, user_id, "User not found")
    else:
        client = get_object_by_id(db, Client, message.client_id, "Client not found")

    db_message = Message(
        chat_id=message.chat_id,
        created_date=message.created_date,
        message=message.message,
        user_id=user_id,
        client_id=message.client_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    if message.client_id is None:
        await send_to_bot(db_message, user.name)
    else:
        await send_to_client(db_message, client)
    return db_message

async def create_message(db: Session, message: MessageCreate):
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
        await send_to_bot(db_message, user.name)
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
            print(f"\033[32mINFO:\033[0m     Message successfully sent to chat_id {chat_id}")
        else:
            print(f"\033[91mERROR:\033[0m    Failed to send message. Status code: "
                  f"{response.status_code}, Response: {response.text}")


async def send_to_client(db_message: Message, client: Client):
    from app.main import sio

    client_data = {
        "id": client.id,
        "name": client.name,
        "cpf": client.cpf,
        "phone_number": client.phone_number,
        "city": client.city,
        "address": client.address,
        "is_active": client.is_active
    }

    created_date_str = db_message.created_date.isoformat()

    await sio.emit("new_message_to_web", {
        "id": db_message.id,
        "chat_id": db_message.chat_id,
        "message": db_message.message,
        "created_date": created_date_str,
        "client_id": db_message.client_id,
        "user_id": db_message.user_id,
        "client": client_data
    })


async def send_broadcast_message(db: Session, message: str, user_id: int):
    clients = db.query(Client.chat_id).filter(Client.chat_id.isnot(None)).distinct().all()

    if not clients:
        print(f"\033[33mWARNING:\033[0m  No chats found. Aborting broadcast.")
        return

    chat_ids = [chat_id[0] for chat_id in clients]

    user = get_object_by_id(db, User, user_id, "User not found")
    user_name = user.name

    escaped_user_name = escape_markdown(user_name)
    escaped_message = escape_markdown(message)

    formatted_message = f"*{escaped_user_name}:*\n{escaped_message}"

    async with httpx.AsyncClient() as client:
        tasks = []
        for chat_id in chat_ids:
            task_payload = {
                'chat_id': chat_id,
                'text': formatted_message,
                'parse_mode': 'Markdown'
            }
            task = client.post(TELEGRAM_API_URL, params=task_payload)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for chat_id, response in zip(chat_ids, responses):
            if response.status_code == 200:
                print(f"\033[32mINFO:\033[0m     Message successfully sent to chat_id: {chat_id}")
            else:
                print(f"\033[91mERROR:\033[0m    Failed to send message to chat_id: {chat_id}. "
                      f"Status code: {response.status_code}, Response: {response.text}")

    return {"message": "Broadcast completed"}


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

def get_active_conversations(db: Session):
    subquery = (
        db.query(
            Message.chat_id,
            func.max(Message.id).label('max_id')
        ).group_by(Message.chat_id).subquery()
    )

    latest_messages = (
        db.query(Message)
        .join(subquery, and_(Message.chat_id == subquery.c.chat_id, Message.id == subquery.c.max_id))
        .options(joinedload(Message.client))
        .order_by(Message.created_date.desc())
        .all()
    )

    conversations = []
    for message in latest_messages:
        conversation = {
            "chat_id": message.chat_id,
            "last_message": message.message,
            "last_message_date": message.created_date,
            "client_id": message.client_id,
            "client_name": message.client.name if message.client else None,
            "status": message.status
        }
        conversations.append(conversation)
    return conversations

def mark_messages_as_read(db: Session, chat_id: int):
    messages = db.query(Message).filter(Message.chat_id == chat_id, Message.status == 'unread').all()
    for message in messages:
        message.status = 'read'
    db.commit()
    return {"message": "Messages marked as read"}
