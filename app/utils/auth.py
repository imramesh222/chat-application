from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.repo.datasource import DataSource
from app.repo.user_repo import UserRepo
from app.model.user_record import UserRecord
import os

# Security scheme
security = OAuth2PasswordBearer(tokenUrl="/auth/token")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

def get_db():
    db = DataSource()
    session = db.get_session()
    try:
        yield session
    finally:
        db.close_session(session)

def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> UserRecord:
    """
    Validate JWT token and return current authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str) or not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user_repo = UserRepo()
    user = user_repo.get_by_email(db, email)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: UserRecord = Depends(get_current_user)) -> UserRecord:
    """
    Ensure user is active (you can add additional checks here)
    """
    # Add any additional user validation logic here
    # For example, check if user is not banned, etc.
    return current_user 

def require_admin(current_user: UserRecord = Depends(get_current_user)) -> UserRecord:
    if not current_user.role or current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user 