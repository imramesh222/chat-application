# Domain logic for authentication
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.domain.common import BaseResponse
from app.domain.user import User

class Session(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    ttl: int = 0
    expiry: Optional[datetime] = None
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    user: Optional[User] = None


class LoginResponse(BaseResponse):
    session: Optional[Session] = None
    dashboard: Optional[str] = None  # 'business' or 'user'


class LogoutResponse(BaseResponse):
    pass


class AuthResponse(BaseResponse):
    session: Optional[Session] = None
