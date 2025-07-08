# Domain logic for messages 
from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[str] = None
    content: str
    user_id: str
    room_id: str
    username: Optional[str] = None  # If you want to include sender's username