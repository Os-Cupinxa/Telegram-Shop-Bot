from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False)
    status = Column(String(255), nullable=False)
    amount = Column(BigInteger, nullable=False)

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
