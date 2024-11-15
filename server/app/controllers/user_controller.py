from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.services import user_service
from app.config.database import get_db
from app.utils.access_token import get_current_user

router = APIRouter()


@router.post("/users/", tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service.create_user(db, user)
    return {"message": "User created successfully"}


@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", tags=["Users"])
def read_users(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    users = user_service.get_all_users(db)
    return users

@router.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user_service.put_user(db, user_id, user)
    return {"message": "User updated successfully"}
