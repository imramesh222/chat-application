# Room API routes 
from fastapi import APIRouter, HTTPException, Depends, Query
from app.domain.room_req_res import (
    CreateRoomRequest, CreateRoomResponse,
    UpdateRoomRequest, UpdateRoomResponse,
    ListRoomRequest, ListRoomResponse,
    GetRoomRequest, GetRoomResponse,
    DeleteRoomRequest, DeleteRoomResponse
)
from app.service.room_service import RoomService
from app.utils import loggerutil
from app.repo.datasource import DataSource
from app.repo.room_repo import RoomRepo
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/room", tags=["Rooms"])

room_repo = RoomRepo()
room_service = RoomService(room_repo)
logger = loggerutil.get_logger(__name__)
db = DataSource()

@router.post("/", response_model=CreateRoomResponse, dependencies=[Depends(require_admin)])
def create_room(request: CreateRoomRequest, current_user=Depends(require_admin)):
    session = db.get_session()
    try:
        return room_service.create_room(session, request=request)
    finally:
        db.close_session(session)

@router.get("/rooms", response_model=ListRoomResponse)
def list_rooms(skip: int = Query(0), limit: int = Query(10), current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        # TODO: Implement list_rooms in RoomService
        return room_service.list_rooms(session, skip=skip, limit=limit)
    finally:
        db.close_session(session)

@router.get("/{room_id}", response_model=GetRoomResponse)
def get_room(room_id: str, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        # TODO: Implement get_room in RoomService
        return room_service.get_room(session, room_id=room_id)
    finally:
        db.close_session(session)

@router.patch("/{room_id}", response_model=UpdateRoomResponse, dependencies=[Depends(require_admin)])
def update_room(room_id: str, request: UpdateRoomRequest, current_user=Depends(require_admin)):
    session = db.get_session()
    try:
        # TODO: Implement update_room in RoomService
        return room_service.update_room(session, room_id=room_id, request=request)
    finally:
        db.close_session(session)

@router.delete("/{room_id}", response_model=DeleteRoomResponse, dependencies=[Depends(require_admin)])
def delete_room(room_id: str, current_user=Depends(require_admin)):
    session = db.get_session()
    try:
        # TODO: Implement delete_room in RoomService
        return room_service.delete_room(session, room_id=room_id)
    finally:
        db.close_session(session)