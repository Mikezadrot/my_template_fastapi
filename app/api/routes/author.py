from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.book_schema import AuthorCreate, AuthorRead
from app.services.author_service import create_author, get_all_authors, get_author_by_id, delete_author
from app.db.database import get_session
from app.core.security import get_current_user, get_admin_user, role_required
from app.models.user import User

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/", response_model=AuthorRead)
def create(author: AuthorCreate, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return create_author(db, author)


@router.get("/", response_model=list[AuthorRead])
def read_all(db: Session = Depends(get_session)):
    return get_all_authors(db)


@router.get("/{author_id}", response_model=AuthorRead)
def read(author_id: int, db: Session = Depends(get_session)):
    return get_author_by_id(db, author_id)


@router.delete("/{author_id}")
def delete(author_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return delete_author(db, author_id)
