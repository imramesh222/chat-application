from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from app.settings import settings
from app.repo.user_repo import UserRepo
from app.repo.room_repo import RoomRepo
from app.utils.auth import get_db
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from app.model.message_record import MessageRecord
from app.model.user_record import UserRecord
from datetime import datetime
import uuid

router = APIRouter()

# In-memory room connections: {room_id: [WebSocket, ...]}
room_connections: Dict[str, List[WebSocket]] = {}

def get_user_from_token(token: str, db: Session) -> Optional[UserRecord]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str) or not email:
            return None
        user = db.query(UserRecord).filter(UserRecord.email == email).first()
        return user
    except JWTError:
        return None

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    print(f"WebSocket connection started for room {room_id}")
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        auth_header = websocket.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:]
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user = get_user_from_token(token, db)
    if not user or not hasattr(user, "full_name"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    if room_id not in room_connections:
        room_connections[room_id] = []
    room_connections[room_id].append(websocket)
    try:
        # 1. Fetch and send recent messages from DB (e.g., last 50)
        recent_messages = db.query(MessageRecord).filter(MessageRecord.room_id == str(room_id)).order_by(MessageRecord.created_at.desc()).limit(50).all()
        for msg in reversed(recent_messages):  # Send oldest first
            sender = db.query(UserRecord).filter_by(id=msg.user_id).first()
            await websocket.send_json({
                "id": msg.id,
                "content": msg.content,
                "user_id": msg.user_id,
                "room_id": msg.room_id,
                "full_name": sender.full_name if sender else None,
                "created_at": msg.created_at.isoformat(),
                "updated_at": msg.updated_at.isoformat()
            })
        while True:
            print("Waiting to receive message...")
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            # 2. Store incoming message in DB
            new_msg = MessageRecord(
                id=str(uuid.uuid4()),
                content=data,
                user_id=user.id,
                room_id=str(room_id),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)
            msg_payload = {
                "id": new_msg.id,
                "content": new_msg.content,
                "user_id": new_msg.user_id,
                "room_id": new_msg.room_id,
                "full_name": user.full_name,
                "created_at": new_msg.created_at.isoformat(),
                "updated_at": new_msg.updated_at.isoformat()
            }
            for conn in room_connections[room_id]:
                await conn.send_json(msg_payload)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for room {room_id}")
        room_connections[room_id].remove(websocket)
        if not room_connections[room_id]:
            del room_connections[room_id]
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
