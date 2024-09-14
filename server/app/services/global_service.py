from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_object_by_id(db: Session, model, object_id: int, error_message: str):
    obj = db.query(model).filter(model.id == object_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail=error_message)
    return obj
