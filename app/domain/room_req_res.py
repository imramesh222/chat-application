from typing import Optional, List
from pydantic import BaseModel
from app.domain.room import Room


class BaseResponse(BaseModel):
    error: bool = False
    msg: Optional[str] = None


class CreateRoomRequest(BaseModel):
    room: Room


class CreateRoomResponse(BaseResponse):
    room: Optional[Room] = None


class UpdateRoomRequest(BaseModel):
    room_id: str
    room: Room


class UpdateRoomResponse(BaseResponse):
    room: Optional[Room] = None


class ListRoomRequest(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10


class ListRoomResponse(BaseResponse):
    rooms: Optional[List[Room]] = None


class GetRoomRequest(BaseModel):
    room_id: str


class GetRoomResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    room: Optional[Room] = None


class DeleteRoomRequest(BaseModel):
    room_id: str


class DeleteRoomResponse(BaseResponse):
    success: bool = False
    msg: Optional[str] = None