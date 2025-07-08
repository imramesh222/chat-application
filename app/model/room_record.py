# SQLAlchemy model for Room
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.repo.datasource import Base

class RoomRecord(Base):
    __tablename__ = "rooms"
    id = Column(String(255), primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    admin_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    messages = relationship("MessageRecord", back_populates="room")