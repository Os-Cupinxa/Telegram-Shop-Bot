from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.config.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    photo_url = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(BigInteger, nullable=False)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
