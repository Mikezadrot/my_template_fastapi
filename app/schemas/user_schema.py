from pydantic import BaseModel
from typing import List, Optional

from uuid import uuid4

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    model_config = {
        "extra": "forbid"
    }


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