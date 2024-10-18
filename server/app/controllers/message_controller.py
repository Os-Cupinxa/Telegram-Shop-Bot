from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.message_schema import MessageCreate, MessageResponse
from app.services import message_service
from app.config.database import get_db

router = APIRouter()


@router.get("/messages/", response_model=List[MessageResponse], tags=["Messages"])
def read_messages(db: Session = Depends(get_db)):
    return message_service.get_all_messages(db)


@router.get("/messages/{message_id}", response_model=MessageResponse, tags=["Messages"])
def read_message(message_id: int, db: Session = Depends(get_db)):
    return message_service.get_message(db, message_id)


@router.post("/messages/", response_model=MessageResponse, tags=["Messages"])
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(db, message)


@router.put("/messages/", response_model=MessageResponse, tags=["Messages"])
def update_message(message_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    return message_service.update_message(db, message_id, message)


@router.delete("/messages/{message_id}", tags=["Messages"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    return message_service.delete_message(db, message_id)
