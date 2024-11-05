from sqlalchemy.orm import Session

from app.models import Product
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate
from app.services.global_service import get_object_by_id


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    return db_category


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name, emoji=category.emoji)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    db_category.name = category.name
    db_category.emoji = category.emoji
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_object_by_id(db, Category, category_id, "Category not found")

    products = db.query(Product).filter(Product.category_id == category_id).first()

    if products:
        return {"error": "Cannot delete category. There are products associated with this category."}

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted"}
