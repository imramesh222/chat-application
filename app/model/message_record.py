from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.repo.datasource import Base

class MessageRecord(Base):
    __tablename__ = "messages"
    id = Column(String(255), primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    room_id = Column(String(255), ForeignKey("rooms.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("UserRecord", back_populates="messages")
    room = relationship("RoomRecord", back_populates="messages")