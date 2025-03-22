from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional, List

from app.schemas.book_schema import BookCreate, BookRead, BookUpdate
from app.services.book_service import (
    create_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
)
from app.db.database import get_session
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookRead)
def create(
    book: BookCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_book(db, book)


@router.get("/", response_model=list[BookRead])
def read_all(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    genre_names: Optional[List[str]] = Query(None),
    sort_by: str = Query("title", enum=["title", "published_year"]),
    current_user: User = Depends(get_current_user)
):
    return get_all_books(db, skip, limit, title, author_id, genre_names, sort_by)


@router.get("/{book_id}", response_model=BookRead)
def read(
    book_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return get_book_by_id(db, book_id)


@router.put("/{book_id}", response_model=BookRead)
def update(
    book_id: int,
    updates: BookUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_book(db, book_id, updates)


@router.delete("/{book_id}")
def delete(
    book_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return delete_book(db, book_id)
