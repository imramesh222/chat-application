# Message service for message business logic 
from app.repo.message_repo import MessageRepo
from app.model.message_record import MessageRecord
from app.domain.message_req_res import CreateMessageRequest, CreateMessageResponse
from app.domain.message import Message as MessageDomain
from app.utils import loggerutil
from typing import List
from app.domain.message_req_res import ListMessageResponse

class MessageService:
    def __init__(self, message_repo: MessageRepo):
        self.message_repo = message_repo
        self.logger = loggerutil.get_logger(self.__class__.__name__)

    def create_message(self, db, request: CreateMessageRequest, user_id: str, room_id: str = None) -> CreateMessageResponse:
        message = MessageRecord(
            content=request.message.content,
            user_id=user_id,
            room_id=room_id or request.message.room_id
        )
        created_message = self.message_repo.create(db, message)
        # Convert to domain model for response
        message_domain = MessageDomain(
            id=getattr(created_message, 'id', None),
            content=getattr(created_message, 'content', None),
            user_id=getattr(created_message, 'user_id', None),
            room_id=getattr(created_message, 'room_id', None),
            created_at=getattr(created_message, 'created_at', None)
        )
        return CreateMessageResponse(message=message_domain)

    def list_messages(self, db, room_id: str, skip: int = 0, limit: int = 50) -> ListMessageResponse:
        # TODO: Implement actual skip/limit in repo if needed
        messages = self.message_repo.get_recent_by_room(db, room_id, limit)
        message_domains = [
            MessageDomain(
                id=getattr(m, 'id', None),
                content=getattr(m, 'content', None),
                user_id=getattr(m, 'user_id', None),
                room_id=getattr(m, 'room_id', None),
                created_at=getattr(m, 'created_at', None)
            ) for m in messages
        ]
        return ListMessageResponse(messages=message_domains)