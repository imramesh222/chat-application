# Domain logic for rooms 
from typing import Optional
from pydantic import BaseModel

 
class Room(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    admin_id: Optional[str] = None
