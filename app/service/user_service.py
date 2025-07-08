from app.domain.common import ErrorCode
from app.domain.user_req_res import (
    CreateUserRequest, CreateUserResponse,
    ListUserResponse,
    GetUserRequest, GetUserResponse,
    UpdateUserRequest, UpdateUserResponse, 
    UpdateUserPasswordRequest, UpdateUserPasswordResponse, 
    ListUserRequest
)
from app.repo.user_repo import UserRepo
from app.service.auth_service import AuthService
from app.utils import loggerutil
from app.utils.hashing import Hash
from app.utils.strutil import is_empty
from app.domain.user import User
from app.mapper.user_mapper import user_mapper

class UserService:
    def __init__(self, auth_service: AuthService, user_repo: UserRepo):
        self.auth_service = auth_service
        self.user_repo = user_repo
        self.logger = loggerutil.get_logger(self.__class__.__name__)

    def create_user(self, req: CreateUserRequest) -> CreateUserResponse:
        self.logger.debug("Creating new user")
        if not req.user:
            return CreateUserResponse(error=True, msg="User data is required")
        if not req.password:
            return CreateUserResponse(error=True, msg="Password is required")
        if is_empty(req.user.email):
            return CreateUserResponse(error=True, msg="Email is required")
        if is_empty(req.user.full_name):
            return CreateUserResponse(error=True, msg="Full name is required")
        existing_user = self.user_repo.get_user_by_email(req.user.email)
        if existing_user:
            return CreateUserResponse(error=True, msg="User already exists")
        user_dict = req.user.dict()
        user_role = user_dict.get('role', 'user')
        user_record = user_mapper.map_user_create_to_user_record(user_dict, req.password, role=user_role)
        created_user = self.user_repo.add_user_record(user_record)
        return CreateUserResponse(error=False, user=created_user)

    def list_users(self, req: ListUserRequest, authorization: str) -> ListUserResponse:
        """List all users with pagination."""
        auth_res = self.auth_service.authorize(authorization)
        if not auth_res:
            return ListUserResponse(error=True, code=ErrorCode.INTERNAL_ERROR, msg="Unauthorized")

        users = self.user_repo.list_users(skip=req.skip or 0, limit=req.limit or 10)
        if not users:
            return ListUserResponse(error=True, code=ErrorCode.NOT_FOUND, msg="No users found")

        self.logger.debug(f"Users found: {users}")
        return ListUserResponse(error=False, users=users)

    def get_user_by_id(self, req: GetUserRequest, authorization: str) -> GetUserResponse:
        """Get a user by ID after authorization."""
        auth_res = self.auth_service.authorize(authorization)
        if not auth_res:
            return UpdateUserResponse(error=True, msg="Unauthorized")      
        user_record = self.user_repo.get_user_by_id(req.id)
        if not user_record:
            return GetUserResponse(error=True, code=ErrorCode.NOT_FOUND, msg="User not found")

        self.logger.debug(f"User found: {user_record}")
        return GetUserResponse(error=False, user=user_record)

    def update_user(self, req: UpdateUserRequest, authorization: str) -> UpdateUserResponse:
        auth_res = self.auth_service.authorize(authorization)
        if not auth_res:
            return UpdateUserResponse(error=True, msg="Unauthorized")
        user = self.user_repo.get_user_by_id(req.id)
        if not user:
            return UpdateUserResponse(error=True, msg="User not found")
        updated_user = self.user_repo.update_user(req.id, req.user)
        return UpdateUserResponse(error=False, user=updated_user)

    def update_user_password(self, user_id: str, req: UpdateUserPasswordRequest) -> UpdateUserPasswordResponse:
        user_record = self.user_repo.get_user_record_by_id(user_id)
        if not user_record:
            return UpdateUserPasswordResponse(success=False, msg="User not found")
        password_hash = str(user_record.password) if user_record.password is not None else None
        if not password_hash or not Hash.verify(req.old_password, password_hash):
            return UpdateUserPasswordResponse(success=False, msg="Old password is incorrect")
        if req.new_password != req.confirm_password:
            return UpdateUserPasswordResponse(success=False, msg="Passwords do not match")
        hashed_new_password = Hash.hash(req.new_password)
        self.user_repo.update_user_password(user_id, hashed_new_password)
        return UpdateUserPasswordResponse(success=True, msg="Password updated successfully")