from sqlmodel import Session
from bcrypt import hashpw, gensalt

from app.schemas.user_schema import UserCreate, GroupCreate
from app.models.user import User, Group, UserGroupLink


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hashpw(user_data.password.encode(), gensalt()).decode()
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_group(db: Session, group_data: GroupCreate):
    new_group = Group(name=group_data.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def add_user_to_group(db: Session, user_id: int, group_id: int):
    try:
        link = UserGroupLink(user_id=user_id, group_id=group_id)
        db.add(link)
        db.commit()
        return "Success"
    except Exception as e:
        print(e)
        return "Error add_user_to_group"
