from pydantic import BaseModel
from typing import List

from uuid import uuid4

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    groups: List[str] = []

class GroupCreate(BaseModel):
    name: str