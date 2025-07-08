from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from app.settings import settings
from app.repo.user_repo import UserRepo
from app.repo.room_repo import RoomRepo
from app.utils.auth import get_db
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from app.model.user_record import UserRecord

router = APIRouter()

# In-memory room connections: {room_id: [WebSocket, ...]}
room_connections: Dict[int, List[WebSocket]] = {}

def get_user_from_token(token: str, db: Session) -> Optional[UserRecord]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str) or not email:
            return None
        user = UserRepo().get_user_by_email(db, email)
        return user
    except JWTError:
        return None

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    # Accept connection first to read headers/query
    await websocket.accept()
    # Get token from query param or header
    token = websocket.query_params.get("token")
    if not token:
        auth_header = websocket.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:]
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user = get_user_from_token(token, db)
    if not user or not hasattr(user, "username"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # Check if room exists
    room = RoomRepo().get_by_name(db, room_id) if isinstance(room_id, str) else RoomRepo().get_by_name(db, str(room_id))
    # For now, skip room existence check if not implemented
    # Add connection to room
    if room_id not in room_connections:
        room_connections[room_id] = []
    room_connections[room_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all in the room
            for conn in room_connections[room_id]:
                if conn != websocket:
                    await conn.send_text(f"{user.username}: {data}")
    except WebSocketDisconnect:
        room_connections[room_id].remove(websocket)
        if not room_connections[room_id]:
            del room_connections[room_id]
