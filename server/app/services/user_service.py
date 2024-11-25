from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Gerar a senha hashada
    hashed_password = get_password_hash(user.password)

    # Criar o novo usuário
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}


def get_user(db: Session, user_id: int):
    return db.query(User).filter(and_(User.id == user_id)).first()

def get_all_users(db: Session):
    return db.query(User).all()

def put_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_user.name = user.name
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    db.commit()
    db.refresh(db_user)

    return {"message": "User updated successfully"}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.email == username).first()
    if user and verify_password(password, user.password):
        return user
    return None
