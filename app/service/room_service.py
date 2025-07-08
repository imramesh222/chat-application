# Room service for room business logic 
from app.repo.room_repo import RoomRepo
from app.model.room_record import RoomRecord
from app.domain.room_req_res import CreateRoomRequest, CreateRoomResponse
from app.domain.room import Room as RoomDomain
from app.utils import loggerutil

class RoomService:
    def __init__(self, room_repo: RoomRepo):
        self.room_repo = room_repo
        self.logger = loggerutil.get_logger(self.__class__.__name__)

    def create_room(self, db, request: CreateRoomRequest) -> CreateRoomResponse:
        room = RoomRecord(
            name=request.room.name,
            description=request.room.description
        )
        created_room = self.room_repo.create(db, room)
        # Convert to domain model for response
        room_domain = RoomDomain(
            id=getattr(created_room, 'id', None),
            name=getattr(created_room, 'name', None),
            description=getattr(created_room, 'description', None),
            created_at=getattr(created_room, 'created_at', None)
        )
        return CreateRoomResponse(room=room_domain)