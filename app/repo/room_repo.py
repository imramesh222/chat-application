from sqlalchemy.orm import Session
from app.model.room_record import RoomRecord

class RoomRepo:
    def get_by_name(self, db: Session, name: str):
        return db.query(RoomRecord).filter(RoomRecord.name == name).first()

    def create(self, db: Session, room: RoomRecord):
        db.add(room)
        db.commit()
        db.refresh(room)
        return room