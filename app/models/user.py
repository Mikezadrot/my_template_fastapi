from sqlmodel import  Field, SQLModel, Relationship
from app.models.base import BaseModel
from typing import Optional, List

# from uuid import uuid4, UUID


class UserGroupLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    group_id: Optional[int] = Field(default=None, foreign_key="group.id", primary_key=True)

class Group(BaseModel, table=True):
    __tablename__ = "group"
    id: Optional[int] =Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, nullable=False)

    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupLink)


class User(BaseModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    groups: List["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
