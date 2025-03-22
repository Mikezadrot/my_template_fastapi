from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.user_schema import UserCreate, GroupCreate, UserUpdate
from app.db.database import get_session
from app.services import user_service
from app.services.user_service import create_user, create_group, add_user_to_group
from app.core.security import get_current_user, get_admin_user
from app.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])

# @router.post("/")
# def register(user: UserCreate, db: Session = Depends(get_session)):
#     return create_user(db=db, user_data=user)

@router.get("/")
def all_users(db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    data =  user_service.get_all_users(db=db)
    return data

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    data = user_service.get_user_by_id(user_id=user_id, db=db)
    if data:
        return user_service.get_user_safe_data(data)
    else:
        return {"msg": "user not existed"}

@router.patch("/{user_id}")
def patch_user_by_id(user_id: int, updates: UserUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return user_service.update_user(user_id=user_id, updates=updates, db=db)

@router.post("/{user_id}/delete")
def delete_user_by_id(user_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return user_service.delete_user(user_id=user_id, db=db)

@router.post("/groups/")
def create_new_group(group: GroupCreate, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return create_group(db=db, group_data=group)

@router.post("/{user_id}/groups/{group_id}/")
def assign_user_to_group(user_id: int, group_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    result = add_user_to_group(
        db=db,
        user_id=user_id,
        group_id=group_id
    )
    return {"msg": f"User added to group: {result}"}


@router.get("/admin")
def admin_area(user: User = Depends(get_admin_user)):
    return {"msg": "Welcome, admin!"}