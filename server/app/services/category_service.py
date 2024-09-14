from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate
from app.services.global_service import get_object_by_id


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    return db_category


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted"}
