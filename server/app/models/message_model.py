from sqlalchemy import Column, Integer, String, Text
from app.config.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
