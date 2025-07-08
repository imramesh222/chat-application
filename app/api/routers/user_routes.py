# User API routes 
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.routers.auth_routes import get_authorization_token
from app.domain.common import ErrorCode
from app.domain.user_req_res import (
    CreateUserRequest, CreateUserResponse,
    ListUserRequest, ListUserResponse,
    GetUserResponse, GetUserRequest,
    UpdateUserRequest, UpdateUserResponse,
    UpdateUserPasswordRequest, UpdateUserPasswordResponse
)
from app.repo.user_repo import UserRepo
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.utils import loggerutil
from app.repo.datasource import DataSource

router = APIRouter(prefix="/user", tags=["Users"])


db = DataSource()
user_repo = UserRepo(db=db)
auth_service = AuthService(user_repo=user_repo)
user_service = UserService(auth_service=auth_service, user_repo=user_repo)  # Pass minio_client

logger = loggerutil.get_logger(__name__)

@router.post("/signup", response_model=CreateUserResponse)
def signup_user(req: CreateUserRequest):
    print("Signup endpoint called")
    session = db.get_session()
    try:
        response = user_service.create_user(req)
        return response
    finally:
        db.close_session(session)

@router.get("/users", response_model=ListUserResponse)
def get_all_users(
        authorization: str = Depends(get_authorization_token),
        skip: int = Query(0, description="Number of users to skip"),
        limit: int = Query(10, description="Maximum number of users to return")
):
    try:
        req = ListUserRequest(skip=skip, limit=limit)
        res = user_service.list_users(req, authorization)
        return res
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        return ListUserResponse(error=True, msg=str(e))

@router.get("/{user_id}", response_model=GetUserResponse)
def get_user(user_id: str, authorization: str = Depends(get_authorization_token)):
    try:
        req = GetUserRequest(id=user_id)
        return user_service.get_user_by_id(req, authorization)
    except Exception as e:
        logger.exception(f"Error: {e}")
        return GetUserResponse(error=True, msg=str(e))


@router.put("/update/{user_id}", response_model=UpdateUserResponse)
def update_user(
    user_id: str,
    req: UpdateUserRequest,
    authorization: str = Depends(get_authorization_token)
):
    try:
        req.id = user_id
        res = user_service.update_user(req, authorization)
        return res
    except Exception as e:
        logger.exception(f"Error: {e}")
        return UpdateUserResponse(error=True, msg=str(e))

@router.post("/update_password", response_model=UpdateUserPasswordResponse)
def update_password(
    req: UpdateUserPasswordRequest,
    authorization: str = Depends(get_authorization_token)
):
    # Extract user info from token
    user_info = user_service.auth_service.authorize(authorization)
    if not user_info or not user_info.session or not user_info.session.user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = user_info.session.user.id

    response = user_service.update_user_password(user_id, req)
    if not response.success:
        raise HTTPException(status_code=400, detail=response.msg)
    return response