# Domain logic for messages 
from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[str] = None
    content: str
    user_id: Optional[str] = None
    room_id: Optional[str] = None
    full_name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
