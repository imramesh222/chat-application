from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import os
import jwt

from app.domain.common import ErrorCode
from app.domain.auth import Session, LoginResponse, AuthResponse, LogoutResponse
from app.domain.user import User
from app.repo.datasource import DataSource
from app.repo.user_repo import UserRepo
from app.utils import loggerutil
from app.utils.hashing import Hash
from app.utils.singleton import Singleton

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60

logger = loggerutil.get_logger(__name__)


class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def add_session(self, email: str, token: str, expires: datetime) -> None:
        self.sessions[token] = Session(email=email, expiry=expires, access_token=token)

    def get_session(self, token: str) -> Optional[Session]:
        session = self.sessions.get(token, None)
        if session and session.expiry and session.expiry < datetime.now():
            self.remove_session(token)
            return None
        return session

    def remove_session(self, token: str) -> Optional[Session]:
        return self.sessions.pop(token, None)

    def cleanup_expired(self) -> None:
        current_time = datetime.now()
        expired = [token for token, session in self.sessions.items() 
                  if session.expiry and session.expiry < current_time]
        for token in expired:
            self.remove_session(token)

def _decode_jwt(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return None


class AuthService(metaclass=Singleton):
    _instance = None

    def __init__(self, user_repo: UserRepo) -> None:
        if AuthService._instance is not None:
            return
        self.user_repo = user_repo
        self.session_store = SessionStore()

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate the user by email and password."""
        user_record = self.user_repo.get_user_by_email(email)
        if not user_record:
            return None
        
        password_hash = str(user_record.password) if user_record.password is not None else None
        if not password_hash:
            return None
            
        if not Hash.verify(password, password_hash):
            return None
        from app.repo.user_repo import _map_user_record_to_user
        return _map_user_record_to_user(user_record)

    def login(self, email: str, password: str) -> LoginResponse:
        """Log in the user and create a session."""
        user = self.authenticate(email, password)
        if user is None:
            return LoginResponse(error=True, code=ErrorCode.UNAUTHORIZED, msg="Invalid username or password")

        session = self._create_access_token(email)
        session.user = user
        user_record = self.user_repo.get_user_by_email(email)
        if user_record and user_record.role is not None:
            session.role = str(user_record.role)
        else:
            session.role = "user"
        dashboard = "business" if session.role == "business" else "user"
        return LoginResponse(error=False, session=session, dashboard=dashboard)

    def _create_access_token(self, email: str, expires_delta: Optional[timedelta] = None) -> Session:
        """Create a JWT access token for the user."""
        expire = datetime.now() + (expires_delta or timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRE_SECONDS))
        to_encode = {"sub": email, "exp": expire}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        self.session_store.add_session(email=email, token=token, expires=expire)
        return Session(
            access_token=token,
            token_type="bearer",
            ttl=JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
            expiry=expire,
            username=email
        )

    def _authorize(self, token: str) -> Tuple[Optional[ErrorCode], Optional[str], Optional[Session]]:
        """Authorize the user based on the provided token."""
        if not token:
            return ErrorCode.UNAUTHORIZED, "Invalid token", None

        payload = _decode_jwt(token)
        if payload is None:
            return ErrorCode.UNAUTHORIZED, "Invalid token", None

        session = self.session_store.get_session(token)
        if not session or session.access_token != token:
            return ErrorCode.UNAUTHORIZED, "Unauthorized", None

        username = payload.get("sub")
        if not username:
            return ErrorCode.UNAUTHORIZED, "Invalid token payload", None
            
        user_record = self.user_repo.get_user_by_email(username)
        if user_record is None:
            return ErrorCode.UNAUTHORIZED, "User does not exist", None
        from app.repo.user_repo import _map_user_record_to_user
        session.user = _map_user_record_to_user(user_record)
        session.role = str(user_record.role) if user_record.role is not None else "user"
        return None, None, session

    def authorize(self, token: str) -> AuthResponse:
        """Public method to authorize a user."""
        if not token:
            return AuthResponse(error=True, code=ErrorCode.UNAUTHORIZED, msg="Invalid token")
        try:
            code, msg, session = self._authorize(token)
            if code:
                return AuthResponse(error=True, code=code, msg=msg)
            return AuthResponse(error=False, session=session)
        except Exception as e:
            logger.exception(f"Error authorizing token: {e}")
            return AuthResponse(error=True, code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def logout(self, token: str) -> LogoutResponse:
        """Log out the user and remove the session."""
        session = self.session_store.remove_session(token)
        if session is None:
            return LogoutResponse(error=True, code=ErrorCode.NOT_FOUND, msg="Session not found")
        return LogoutResponse(error=False)

    @classmethod
    def get_instance(cls) -> "AuthService":
        """Get a singleton instance of AuthService."""
        if cls._instance is None:
            db = DataSource()
            user_repo = UserRepo(db)
            cls._instance = AuthService(user_repo)
        return cls._instance

    @classmethod
    def generate_token(cls, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Generate a JWT token for the given user ID."""
        expire = datetime.now() + (expires_delta or timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRE_SECONDS))
        to_encode = {"sub": user_id, "exp": expire}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token