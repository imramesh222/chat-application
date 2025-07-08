# SQLAlchemy model for User
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.repo.datasource import Base

class UserRecord(Base):
    __tablename__ = "users"
    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    username = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_pic_url = Column(Text, nullable=True)
    role = Column(String(50), nullable=True, default="user")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    messages = relationship("MessageRecord", back_populates="user")