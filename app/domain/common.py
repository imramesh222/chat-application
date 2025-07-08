from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ErrorCode(Enum):
    UNKNOWN = 0
    INVALID_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    BAD_REQUEST = 400
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    SERVICE_UNAVAILABLE = 503
    RATE_LIMIT_EXCEEDED = 429
    TOO_MANY_REQUESTS = 429
    GATEWAY_TIMEOUT = 504


class Pagination(BaseModel):
    limit: int = 100
    offset: int = 0
    prev_cursor: str = None
    next_cursor: str = None
    total_count: int = 0


class Debug(BaseModel):
    debug_id: Optional[str] = None
    trace_id: Optional[str] = None
    request_id: Optional[str] = None


class BaseRequest(BaseModel):
    authorization: str = None
    debug: Debug = None


class BaseResponse(BaseModel):
    error: bool = False
    code: ErrorCode = ErrorCode.UNKNOWN
    msg: Optional[str] = None


class PublicRequest(BaseModel):
    """For unauthenticated routes like signup (no auth/debug)"""
    pass