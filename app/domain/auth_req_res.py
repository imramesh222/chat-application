from typing import Optional
from pydantic import BaseModel, EmailStr



class UserSignupRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone: str
    password: str
    profile_pic_url: Optional[str] = None

class BusinessUserSignupRequest(UserSignupRequest):
    business_name: str
    business_email: EmailStr
    business_phone: str
    industry_type: Optional[str]
    address: Optional[str]
    role: str  

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
