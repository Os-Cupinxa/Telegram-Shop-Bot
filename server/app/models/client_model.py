from sqlalchemy import Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))
    is_active = Column(Boolean, nullable=False)

    orders = relationship("Order", back_populates="client")
