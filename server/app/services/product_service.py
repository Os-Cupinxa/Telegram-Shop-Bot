from sqlalchemy.orm import Session

from app.models import Category
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate
from app.services.global_service import get_object_by_id


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    db_product = get_object_by_id(db, Product, product_id, "Product not found")

    return db_product


def create_product(db: Session, product: ProductCreate):
    get_object_by_id(db, Category, product.category_id, "Category not found")

    db_product = Product(
        category_id=product.category_id,
        photo_url=product.photo_url,
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = get_object_by_id(db, Product, product_id, "Product not found")
    get_object_by_id(db, Category, product.category_id, "Category not found")

    db_product.category_id = product.category_id
    db_product.status = product.status
    db_product.amount = product.amount
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_object_by_id(db, Product, product_id, "Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}
