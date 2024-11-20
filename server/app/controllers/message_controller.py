from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.message_schema import MessageCreate, MessageResponse, ConversationResponse
from app.services import message_service
from app.config.database import get_db
from app.utils.access_token import get_current_user

from typing import Optional
router = APIRouter()


@router.get("/messages/", response_model=List[MessageResponse], tags=["Messages"])
def read_messages(chat_id: Optional[int] = None, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return message_service.get_all_messages(db, chat_id)



@router.get("/messages/{message_id}", response_model=MessageResponse, tags=["Messages"])
def read_message(message_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return message_service.get_message(db, message_id)


@router.post("/messages/", response_model=MessageResponse, tags=["Messages"])
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = await message_service.create_message(db, message)
    return db_message


@router.post("/broadcast/", tags=["Messages"])
async def send_broadcast(message: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    await message_service.send_broadcast_message(db, message, current_user)


@router.put("/messages/", response_model=MessageResponse, tags=["Messages"])
def update_message(message_id: int, message: MessageCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(get_current_user)):
    return message_service.update_message(db, message_id, message)


@router.delete("/messages/{message_id}", tags=["Messages"])
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return message_service.delete_message(db, message_id)



@router.get("/conversations/", response_model=List[ConversationResponse], tags=["Conversations"])
def get_conversations(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return message_service.get_active_conversations(db)



@router.post("/conversations/{chat_id}/mark_as_read", tags=["Conversations"])
def mark_conversation_as_read(chat_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    result = message_service.mark_messages_as_read(db, chat_id)
    from app.main import sio
    # Emitir evento via Socket.IO
    sio.emit("conversation_marked_as_read", {"chat_id": chat_id})
    return result

