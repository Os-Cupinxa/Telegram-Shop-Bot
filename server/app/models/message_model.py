from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship

from app.config.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, nullable=False)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False)
    message = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    user = relationship("User", back_populates="messages")
    client = relationship("Client", back_populates="messages")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not (self.user_id or self.client_id):
            raise ValueError("Message must be related to either a user or a client.")
