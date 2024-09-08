from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)
    product_name = Column(String(255), nullable=False)
    product_price = Column(BigInteger, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
