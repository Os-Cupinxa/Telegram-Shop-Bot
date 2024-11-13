from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import UserLogin
from app.services import user_service
from app.utils.access_token import create_access_token

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 10080


@router.post("/login/", tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"user_email": db_user.email, "user_id": db_user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
