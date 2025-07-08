# Domain logic for users 
from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_pic_url: Optional[str] = None
    role: Optional[str] = "user"