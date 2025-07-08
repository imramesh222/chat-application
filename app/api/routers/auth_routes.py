# Authentication API routes 
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader, OAuth2PasswordRequestForm
from app.domain.auth import  LoginResponse, LogoutResponse, Session
from app.domain.common import ErrorCode
from app.domain.auth import LoginResponse, Session, LogoutResponse
from app.service.auth_service import AuthService
from app.utils import loggerutil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=True)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Auth"])
auth_service = AuthService.get_instance()


async def get_authorization_token(authorization: str = Depends(oauth2_scheme)):
    print("Authorization: ", authorization)
    return authorization


async def authorize(authorization: str = Depends(oauth2_scheme)):
    res = auth_service.authorize(authorization)
    if res.error:
        raise HTTPException(status_code=res.code.value, detail=res.msg)
    return res.session.user


@router.post("/auth/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = auth_service.login(form_data.username, form_data.password)
        return res
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return LoginResponse(error=True, code=ErrorCode.UNAUTHORIZED, msg=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        return LoginResponse(error=True, code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.post("/auth/token", response_model=Session)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = auth_service.login(form_data.username, form_data.password)
        if res.error:
            logger.error(f"Invalid credentials for user: {form_data.username}")
            raise HTTPException(status_code=res.code.value, detail=res.msg)
        return res.session
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/logout", response_model=LogoutResponse)
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        return auth_service.logout(token)
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return LogoutResponse(error=True, code=ErrorCode.UNAUTHORIZED, msg=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        return LogoutResponse(error=True, code=ErrorCode.INTERNAL_ERROR, msg=str(e))
