import uuid

from app.model.user_record import UserRecord
from app.utils.hashing import Hash
from typing import Dict, Any

def hash_password(password: str) -> str:
    return Hash.hash(password)

def map_user_create_to_user_record(user_dict, plain_password, role="user"):
    return UserRecord(
        id=str(uuid.uuid4()),
        username=user_dict.get("username"),
        email=user_dict.get("email"),
        password=Hash.hash(plain_password),
        role=role,
        full_name=user_dict.get("full_name"),
        phone=user_dict.get("phone"),
        profile_pic_url=user_dict.get("profile_pic_url")
    )

class UserMapper:
    hash_password = staticmethod(hash_password)
    map_user_create_to_user_record = staticmethod(map_user_create_to_user_record)

user_mapper = UserMapper()