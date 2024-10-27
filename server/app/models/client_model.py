from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    cpf = Column(String(11))
    phone_number = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))
    is_active = Column(Boolean, nullable=False, default=True)

    orders = relationship("Order", back_populates="client")
