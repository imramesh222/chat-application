# Room service for room business logic 
from app.repo.room_repo import RoomRepo
from app.model.room_record import RoomRecord
from app.domain.room_req_res import CreateRoomRequest, CreateRoomResponse, DeleteRoomResponse, GetRoomResponse, ListRoomResponse, UpdateRoomResponse
from app.domain.room import Room as RoomDomain
from app.utils import loggerutil
import uuid

class RoomService:
    def __init__(self, room_repo: RoomRepo):
        self.room_repo = room_repo
        self.logger = loggerutil.get_logger(self.__class__.__name__)

    def create_room(self, db, request: CreateRoomRequest, current_user):
        room = RoomRecord(
            id=str(uuid.uuid4()),
            name=request.room.name,
            description=request.room.description,
            admin_id=current_user.id
        )
        created_room = self.room_repo.create(db, room)
        # Convert to domain model for response
        room_domain = RoomDomain(
            id=str(created_room.id),
            name=str(created_room.name),
            description=str(created_room.description) if created_room.description is not None else None,
            admin_id=str(created_room.admin_id) if created_room.admin_id is not None else None
        )
        return CreateRoomResponse(room=room_domain)

    def list_rooms(self, db, current_user, skip=0, limit=10):
        query = db.query(RoomRecord)
        if getattr(current_user, "role", "user") != "admin":
            query = query.filter(RoomRecord.admin_id == current_user.id)
        rooms = query.offset(skip).limit(limit).all()
        rooms_list = [
            RoomDomain(
                id=str(room.id),
                name=str(room.name),
                description=str(room.description) if room.description is not None else None,
                admin_id=str(room.admin_id) if room.admin_id is not None else None
            )
            for room in rooms
        ]
        return ListRoomResponse(rooms=rooms_list)

    def get_room(self, db, room_id, current_user):
        room = db.query(RoomRecord).filter(RoomRecord.id == room_id).first()
        if not room:
            return GetRoomResponse(error=True, msg="Room not found")
        if getattr(current_user, "role", "user") != "admin" and room.admin_id != current_user.id:
            return GetRoomResponse(error=True, msg="Not authorized")
        room_domain = RoomDomain(
            id=str(room.id),
            name=str(room.name),
            description=str(room.description) if room.description is not None else None,
            admin_id=str(room.admin_id) if room.admin_id is not None else None
        )
        return GetRoomResponse(room=room_domain)

    def update_room(self, db, room_id, request, current_user):
        room = db.query(RoomRecord).filter(RoomRecord.id == room_id).first()
        if not room:
            return UpdateRoomResponse(error=True, msg="Room not found")
        if getattr(current_user, "role", "user") != "admin" and room.admin_id != current_user.id:
            return UpdateRoomResponse(error=True, msg="Not authorized")
        # Update fields as needed
        if request.room.name is not None:
            room.name = request.room.name
        if request.room.description is not None:
            room.description = request.room.description
        db.commit()
        db.refresh(room)
        room_domain = RoomDomain(
            id=str(room.id),
            name=str(room.name),
            description=str(room.description) if room.description is not None else None,
            admin_id=str(room.admin_id) if room.admin_id is not None else None
        )
        return UpdateRoomResponse(room=room_domain)

    def delete_room(self, db, room_id, current_user):
        room = db.query(RoomRecord).filter(RoomRecord.id == room_id).first()
        if not room:
            return DeleteRoomResponse(success=False, msg="Room not found")
        if getattr(current_user, "role", "user") != "admin" and room.admin_id != current_user.id:
            return DeleteRoomResponse(success=False, msg="Not authorized")
        db.delete(room)
        db.commit()
        return DeleteRoomResponse(success=True, msg="Room deleted")