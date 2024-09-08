from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user_model import User
from app.schemas.user_schema import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(and_(User.id == user_id)).first()
