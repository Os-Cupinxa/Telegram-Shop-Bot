from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(and_(Category.id == category_id)).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = db.query(Category).filter(and_(Category.id == category_id)).first()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(and_(Category.id == category_id)).first()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted"}
