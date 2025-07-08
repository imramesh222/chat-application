"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 22/04/2025
"""

import re
from typing import Optional


def is_empty(value: Optional[str]) -> bool:
    """Check if a string is empty or None."""
    return value is None or value.strip() == ""


def is_not_empty(value: str) -> bool:
    return not is_empty(value)


def generate_username_from_name(full_name: str) -> str:
    """
    Generate a username from a full name.
    
    Args:
        full_name: The full name to convert to username
        
    Returns:
        str: Generated username in lowercase with underscores
    """
    if not full_name:
        return ""
    
    # Convert to lowercase
    username = full_name.lower()
    
    # Replace spaces and common separators with underscores
    username = re.sub(r'[\s\-\.]+', '_', username)
    
    # Remove special characters except underscores
    username = re.sub(r'[^a-z0-9_]', '', username)
    
    # Remove multiple consecutive underscores
    username = re.sub(r'_+', '_', username)
    
    # Remove leading and trailing underscores
    username = username.strip('_')
    
    return username


def generate_unique_username(base_username: str, existing_usernames: list) -> str:
    """
    Generate a unique username by adding a suffix if the base username already exists.
    
    Args:
        base_username: The base username to check
        existing_usernames: List of existing usernames to check against
        
    Returns:
        str: Unique username
    """
    if not base_username:
        return ""
    
    username = base_username
    counter = 1
    
    while username in existing_usernames:
        username = f"{base_username}_{counter}"
        counter += 1
    
    return username
