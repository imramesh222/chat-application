from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.repo.datasource import DataSource
from app.model.room_record import RoomRecord
from app.model.message_record import MessageRecord
from app.model.user_record import UserRecord
from app.utils.auth import require_admin, get_db
from typing import List, Optional
import csv
import io

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if date_str:
        try:
            return datetime.fromisoformat(date_str)
        except Exception:
            return None
    return None

@router.get("/messages-per-room")
def messages_per_room(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)", alias="start_date"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)", alias="end_date"),
    format: str = Query("json", description="Response format: json or csv")
):
    """
    Returns a list of rooms with the count of messages in each room. Optional date filters. Supports CSV export.
    """
    start = parse_date(start_date)
    end = parse_date(end_date)
    rooms = db.query(RoomRecord).all()
    result = []
    for room in rooms:
        msg_query = db.query(MessageRecord).filter(MessageRecord.room_id == room.id)
        if start:
            msg_query = msg_query.filter(MessageRecord.created_at >= start)
        if end:
            msg_query = msg_query.filter(MessageRecord.created_at <= end)
        message_count = msg_query.count()
        result.append({
            "room_id": room.id,
            "room_name": room.name,
            "message_count": message_count
        })
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["room_id", "room_name", "message_count"])
        writer.writeheader()
        for row in result:
            writer.writerow(row)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=messages_per_room.csv"}
        )
    return {"rooms": result}

@router.get("/user-activity")
def user_activity(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)", alias="start_date"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)", alias="end_date"),
    format: str = Query("json", description="Response format: json or csv")
):
    """
    Returns a list of users with the count of messages sent by each user. Optional date filters. Supports CSV export.
    """
    start = parse_date(start_date)
    end = parse_date(end_date)
    users = db.query(UserRecord).all()
    result = []
    for user in users:
        msg_query = db.query(MessageRecord).filter(MessageRecord.user_id == user.id)
        if start:
            msg_query = msg_query.filter(MessageRecord.created_at >= start)
        if end:
            msg_query = msg_query.filter(MessageRecord.created_at <= end)
        message_count = msg_query.count()
        result.append({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "message_count": message_count
        })
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["user_id", "username", "email", "message_count"])
        writer.writeheader()
        for row in result:
            writer.writerow(row)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=user_activity.csv"}
        )
    return {"users": result}
