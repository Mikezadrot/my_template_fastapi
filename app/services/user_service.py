from sqlmodel import Session, select
from bcrypt import hashpw, gensalt

from app.schemas.user_schema import UserCreate, GroupCreate, UserUpdate
from app.models.user import User, Group, UserGroupLink
from app.utils import exceptions


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = db.exec(statement).first()
    return result

def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()
    return result


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    statement = select(User).offset(skip).limit(limit)
    results = db.exec(statement)
    data = [get_user_safe_data(i) for i in results]

    return data


def get_user_safe_data(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "groups": [g.name for g in user.groups]
    }


def create_user(db: Session, user_data: UserCreate):
    if get_user_by_email(db, user_data.email) or get_user_by_username(db, user_data.username):
        # raise ValueError("User with this email or username already exists")
        raise exceptions.UserAlreadyExistsException
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

# UPDATE
def update_user(db: Session, user_id: int, updates: UserUpdate) -> User | None:
    user = db.get(User, user_id)
    if not user:
        raise exceptions.UserNotFoundException
    try:
        update_data = updates.model_dump(exclude_unset=True)
    except Exception as e:
        raise exceptions.InvalidDataException

    if "username" in update_data:
        existing_user = db.exec(
            select(User).where(User.username == update_data["username"], User.id != user_id)
        ).first()
        if existing_user:
            raise exceptions.InvalidPatchedUsername
        elif len(update_data["username"]) <= 0:
            raise exceptions.InvalidDataException

        # 🔍 Перевірка email
    if "email" in update_data:
        existing_email = db.exec(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        ).first()
        if existing_email:
            raise exceptions.InvalidPatchedEmail
        elif len(update_data["email"]) <= 5:
            raise exceptions.InvalidDataException

    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# DELETE
def delete_user(db: Session, user_id: int) -> bool:
    try:
        user = db.get(User, user_id)
        if not user:
            raise exceptions.UserNotFoundException
        db.delete(user)
        db.commit()
        result = {"detail": "Success delete"}
        return result
    except Exception as e:
        print(e)
        raise exceptions.DeveloperError

def create_group(db: Session, group_data: GroupCreate):
    if get_group_by_name(db=db, name=group_data.name):
        raise exceptions.GroupAlreadyExistsException
    new_group = Group(name=group_data.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

# READ
def get_group_by_id(db: Session, group_id: int) -> Group | None:
    return db.get(Group, group_id)

def get_group_by_name(db: Session, name: str) -> Group | None:
    statement = select(Group).where(Group.name == name)
    result = db.exec(statement).first()
    return result


def get_all_groups(db: Session, skip: int = 0, limit: int = 100):
    statement = select(Group).offset(skip).limit(limit)
    result = db.exec(statement)
    return result.all()

# UPDATE
def update_group(db: Session, group_id: int, updates: dict) -> Group | None:
    group = db.get(Group, group_id)
    if not group:
        return None
    for key, value in updates.items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group

# DELETE
def delete_group(db: Session, group_id: int) -> bool:
    group = db.get(Group, group_id)
    if not group:
        return False
    db.delete(group)
    db.commit()
    return True




def add_user_to_group(db: Session, user_id: int, group_id: int):
    statement = select(UserGroupLink).where(UserGroupLink.user_id == user_id).where(UserGroupLink.group_id == group_id)
    link_exists = db.exec(statement).first()
    # link_exists = db.exec(select(UserGroupLink).where(UserGroupLink.user_id == user_id, UserGroupLink.group_id == group_id
    #     )
    # ).first()

    if link_exists:
        return "User already in group"

    try:
        link = UserGroupLink(user_id=user_id, group_id=group_id)
        db.add(link)
        db.commit()
        return "Success"
    except Exception as e:
        db.rollback()
        return "Error add_user_to_group"


def remove_user_from_group(db: Session, user_id: int, group_id: int):
    statement = select(UserGroupLink).where(UserGroupLink.user_id == user_id).where(UserGroupLink.group_id == group_id)
    link = db.exec(statement).first()
    if not link:
        return "User not in group"

    db.delete(link)
    db.commit()
    return "Removed"
