import jwt
from datetime import datetime, timedelta
from typing import Any

# Secret key for encoding and decoding JWT tokens (you should store this in a secure place, e.g., environment variables)
SECRET_KEY = "15d8f5f31c97b88aa6b303aa437b6e949afadc60b76ecfcbd085df680f4e353e"  # Change this to a strong secret key
ALGORITHM = "HS256"  # You can use different algorithms like RS256 if you prefer
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time (in minutes)

def create_access_token(data: Any, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token with expiration.

    :param data: The data to include in the JWT (usually the user's identifier or email).
    :param expires_delta: Optional expiration time. If not provided, it uses the default expiration time.
    :return: A signed JWT token as a string.
    """
    to_encode = data.copy()  # Make a copy of the data to be encoded into the JWT
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})  # Add expiration to the data

    # Encode the data into a JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """
    Verify a JWT access token and decode it.

    :param token: The JWT token to verify.
    :return: The decoded JWT data if the token is valid, else raises an error.
    """
    try:
        # Decode the JWT token using the SECRET_KEY and the ALGORITHM used for encoding
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload (usually containing user info)
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError as e:
        raise Exception(f"Invalid token: {str(e)}")
