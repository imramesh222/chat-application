import jwt
from datetime import datetime, timedelta
from typing import Any
import os
from jwt.exceptions import ExpiredSignatureError, PyJWTError

# Secret key for encoding and decoding JWT tokens (use environment variable)
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set!")
ALGORITHM = "HS256"  # You can use different algorithms like RS256 if you prefer
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time (in minutes)

def create_access_token(data: Any, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()  # Make a copy of the data to be encoded into the JWT
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Add expiration to the data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload (usually containing user info)
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except PyJWTError as e:
        raise Exception(f"Invalid token: {str(e)}")
