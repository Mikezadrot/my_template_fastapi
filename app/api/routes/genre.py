from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.book_schema import GenreCreate, GenreRead
from app.services.genre_service import create_genre, get_all_genres, get_genre_by_id, delete_genre
from app.db.database import get_session
from app.core.security import get_current_user, get_admin_user, role_required
from app.models.user import User

router = APIRouter(prefix="/genres", tags=["genres"])


@router.post("/", response_model=GenreRead)
def create(genre: GenreCreate, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return create_genre(db, genre)


@router.get("/", response_model=list[GenreRead])
def read_all(db: Session = Depends(get_session)):
    return get_all_genres(db)


@router.get("/{genre_id}", response_model=GenreRead)
def read(genre_id: int, db: Session = Depends(get_session)):
    return get_genre_by_id(db, genre_id)


@router.delete("/{genre_id}")
def delete(genre_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_admin_user)):
    return delete_genre(db, genre_id)