import uuid

def get_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")

def get_int_uuid() -> int:
    return uuid.uuid4().fields[-1]

def generate_uuid(prefix: str = "") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
