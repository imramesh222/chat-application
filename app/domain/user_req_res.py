from typing import Optional, List
from pydantic import BaseModel
from app.domain.user import User


class BaseResponse(BaseModel):
    error: bool = False
    msg: Optional[str] = None


class CreateUserRequest(BaseModel):
    user: User
    password: str


class CreateUserResponse(BaseResponse):
    user: Optional[User] = None


class UpdateUserRequest(BaseModel):
    id: str
    user: User
    # password: Optional[str] = None


class UpdateUserResponse(BaseResponse):
    user: Optional[User] = None


class ListUserRequest(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10


class ListUserResponse(BaseResponse):
    users: Optional[List[User]] = None


class GetUserRequest(BaseModel):
    id: str


class GetUserResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    user: Optional[User] = None


class UpdateUserPasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UpdateUserPasswordResponse(BaseResponse):
    success: bool = False
    msg: Optional[str] = None