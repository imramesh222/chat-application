from typing import Optional, List
from pydantic import BaseModel
from app.domain.message import Message


class BaseResponse(BaseModel):
    error: bool = False
    msg: Optional[str] = None


class CreateMessageRequest(BaseModel):
    message: Message
    user_id: str


class CreateMessageResponse(BaseResponse):
    message: Optional[Message] = None


class UpdateMessageRequest(BaseModel):
    message_id: str
    message: Message


class UpdateMessageResponse(BaseResponse):
    message: Optional[Message] = None


class ListMessageRequest(BaseModel):
    room_id: str
    skip: Optional[int] = 0
    limit: Optional[int] = 50


class ListMessageResponse(BaseResponse):
    messages: Optional[List[Message]] = None


class GetMessageRequest(BaseModel):
    message_id: str


class GetMessageResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    message: Optional[Message] = None


class DeleteMessageRequest(BaseModel):
    message_id: str


class DeleteMessageResponse(BaseResponse):
    success: bool = False
    msg: Optional[str] = None