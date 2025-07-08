# Message repository for database access 
from sqlalchemy.orm import Session  
from app.model.message_record import MessageRecord

class MessageRepo:
    def get_recent_by_room(self, db: Session, room_id: str, limit: int = 50):
        return db.query(MessageRecord).filter(MessageRecord.room_id == room_id).order_by(MessageRecord.created_at.desc()).limit(limit).all()

    def create(self, db: Session, message: MessageRecord):
        db.add(message)
        db.commit()
        db.refresh(message)
        return message