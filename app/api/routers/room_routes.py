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

@router.post("/", response_model=CreateRoomResponse)
def create_room(request: CreateRoomRequest, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        return room_service.create_room(session, request=request, current_user=current_user)
    finally:
        db.close_session(session)

@router.get("/rooms", response_model=ListRoomResponse)
def list_rooms(skip: int = Query(0), limit: int = Query(10), current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        return room_service.list_rooms(session, current_user, skip=skip, limit=limit)
    finally:
        db.close_session(session)

@router.get("/{room_id}", response_model=GetRoomResponse)
def get_room(room_id: str, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        return room_service.get_room(session, room_id, current_user)
    finally:
        db.close_session(session)

@router.patch("/{room_id}", response_model=UpdateRoomResponse)
def update_room(room_id: str, request: UpdateRoomRequest, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        return room_service.update_room(session, room_id, request, current_user)
    finally:
        db.close_session(session)

@router.delete("/{room_id}", response_model=DeleteRoomResponse)
def delete_room(room_id: str, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        return room_service.delete_room(session, room_id, current_user)
    finally:
        db.close_session(session)