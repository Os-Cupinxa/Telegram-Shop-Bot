from datetime import datetime, timedelta, timezone
from typing import Dict

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id
