# Message API routes 
from fastapi import APIRouter, HTTPException, Depends, Query
from app.domain.message_req_res import (
    CreateMessageRequest, CreateMessageResponse,
    ListMessageRequest, ListMessageResponse
)
from app.repo.message_repo import MessageRepo
from app.service.message_service import MessageService
from app.utils import loggerutil
from app.repo.datasource import DataSource
from app.utils.auth import get_current_user

router = APIRouter(prefix="/message", tags=["Messages"])

message_repo = MessageRepo()
message_service = MessageService(message_repo)
logger = loggerutil.get_logger(__name__)
db = DataSource()

@router.post("/", response_model=CreateMessageResponse)
def create_message(request: CreateMessageRequest):
    session = db.get_session()
    try:
        user_id = getattr(request, 'user_id', 1)  # Replace with actual user_id extraction
        return message_service.create_message(session, request=request, user_id=user_id)
    finally:
        db.close_session(session)

@router.post("/rooms/{room_id}/messages", response_model=CreateMessageResponse)
def create_message(room_id: str, request: CreateMessageRequest, current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        # TODO: Implement create_message for room in MessageService
        return message_service.create_message(session, request=request, user_id=current_user.id, room_id=room_id)
    finally:
        db.close_session(session)

@router.get("/rooms/{room_id}/messages", response_model=ListMessageResponse)
def list_messages(room_id: str, skip: int = Query(0), limit: int = Query(50), current_user=Depends(get_current_user)):
    session = db.get_session()
    try:
        # TODO: Implement list_messages for room in MessageService
        return message_service.list_messages(session, room_id=room_id, skip=skip, limit=limit)
    finally:
        db.close_session(session)