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
        name=message.name,
        description=message.description,
        text=message.text
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, message: MessageCreate):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    db_message.name = message.name
    db_message.description = message.description
    db_message.text = message.text
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = get_object_by_id(db, Message, message_id, "Message not found")

    db.delete(db_message)
    db.commit()
    return {"message": "Message deleted"}