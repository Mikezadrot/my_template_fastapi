from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.user_schema import UserCreate, GroupCreate
from app.db.database import get_session
from app.services.user_service import create_user, create_group, add_user_to_group

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def register(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(db=db, user_data=user)

@router.post("/groups/")
def create_new_group(group: GroupCreate, db: Session = Depends(get_session)):
    return create_group(db=db, group_data=group)

@router.post("/{user_id}/groups/{group_id}/")
def assign_user_to_group(user_id: int, group_id: int, db: Session = Depends(get_session)):
    result = add_user_to_group(
        db=db,
        user_id=user_id,
        group_id=group_id
    )
    return {"msg": f"User added to group: {result}"}